import time
import signal
from multiprocessing import Process, Value, Event
from dsp_processor_worker import run_dsp_process
from strip_worker import run_strip_process
from status_led import led_clean_up, set_led_down, set_led_up
from effect_manager import EffectManager
from com_manager import ComManager
from queue_channel import QueueChannel
from effects_factory import add_meter_fx, add_blink_fx, add_cop_fx, add_random_fx, add_scroll_fx
from strip import Strip

def get_effect_manager(strip):
    effect_manager = EffectManager(mode="auto_cycle", time_cycle_duration=60000)
    add_scroll_fx(effect_manager, strip)
    add_meter_fx(effect_manager, strip, "center")
    add_random_fx(effect_manager, strip, "toxy_reaf")
    add_blink_fx(effect_manager, strip, "strobe")
    add_random_fx(effect_manager, strip, "red_shift")
    add_blink_fx(effect_manager, strip, "smooth")
    add_meter_fx(effect_manager, strip, "from_bottom")
    add_random_fx(effect_manager, strip, "BlacK_Magenta_Red")
    add_meter_fx(effect_manager, strip, "sides")
    add_cop_fx(effect_manager, strip)
    return effect_manager

def init_worker():
    # Ignore SIGINT and SIGTERM in worker processes
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

class Visualizer:
    def __init__(self):
        # Use Event instead of Value for better process synchronization
        self.shutdown_event = Event()
        self.processes = []

        # Signal handlers only in main process
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        # Initialize shared values
        self.audio_level = Value('d', 0.0)
        self.loop_delta = Value('d', 0.0)

        # Initialize strips
        self.left_strip = Strip(num_leds=120, gpio_pin=18, dma_channel=10, pwm_channel=0)
        self.right_strip = Strip(num_leds=120, gpio_pin=21, dma_channel=5, pwm_channel=0)

        # Initialize effect managers
        self.fx_manager_left = get_effect_manager(self.left_strip)
        self.fx_manager_right = get_effect_manager(self.right_strip)

        # Initialize communication channels
        self.left_channel = QueueChannel()
        self.right_channel = QueueChannel()

        # Initialize communication manager
        self.com_manager = ComManager([self.fx_manager_left, self.fx_manager_right],
                                    [self.left_channel, self.right_channel])

    def start(self):
        set_led_up()
        # Initialize processes
        self.processes = [
            Process(target=self.worker_process,
                   args=(run_dsp_process, (self.audio_level, self.loop_delta, self.shutdown_event))),
            Process(target=self.worker_process,
                   args=(run_strip_process, (self.audio_level, self.loop_delta, self.fx_manager_left,
                         self.left_channel, self.shutdown_event))),
            Process(target=self.worker_process,
                   args=(run_strip_process, (self.audio_level, self.loop_delta, self.fx_manager_right,
                         self.right_channel, self.shutdown_event)))
        ]

        # Start all processes
        for process in self.processes:
            process.start()

        try:
            while not self.shutdown_event.is_set():
                time.sleep(0.1)
                self.com_manager.update(self.loop_delta.value)
        except KeyboardInterrupt:
            pass  # Let the signal handler deal with it

    @staticmethod
    def worker_process(target_func, args):
        # Set up signal handling for worker
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        # Run the actual worker function
        target_func(*args)

    def handle_shutdown(self, signum, frame):
        if not self.shutdown_event.is_set():
            print("\nReceived shutdown signal...")
            self.shutdown()

    def shutdown(self):
        set_led_down()
        # Signal all processes to stop
        self.shutdown_event.set()
        # time.sleep(0.5)
        self.cleanup()

    def cleanup(self):
        print("Cleaning up...")
        try:
            # Terminate all processes
            for process in self.processes:
                try:
                    if process.is_alive():
                        process.terminate()
                    process.join(timeout=1.0)
                except:
                    pass

            # Clean up LED resources
            led_clean_up()
        except:
            pass

if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.start()
