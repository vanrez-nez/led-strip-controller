import time
from dsp_processor import DSPProcessor

def run_dsp_process(audio_queue):
    dsp = DSPProcessor()
    dsp.start()
    try:
        while True:
            dsp.update()
            audio_queue.put(dsp.level)
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass
    finally:
        dsp.stop()