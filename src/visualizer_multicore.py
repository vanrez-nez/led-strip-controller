import time
from multiprocessing import Process, Queue
from dsp_processor_worker import run_dsp_process
from strip_worker import run_strip_process

if __name__ == "__main__":
    audio_queue = Queue()

    # Start DSP process (reads audio and puts levels into audio_queue)
    dsp_proc = Process(target=run_dsp_process, args=(audio_queue,))
    dsp_proc.start()

    # Start LED process (reads audio levels from audio_queue and updates strip)
    strips_queue = Queue()
    strips_proc = Process(target=run_strip_process, args=(strips_queue, audio_queue))
    strips_proc.start()

    try:
        # Main loop can do other things, send commands, etc.
        while True:
            # For demo, just sleep
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Tell LED process to exit
        strips_queue.put("exit")
        # Stop DSP process
        dsp_proc.terminate()

        # Wait for processes to finish
        dsp_proc.join()
        strips_proc.join()