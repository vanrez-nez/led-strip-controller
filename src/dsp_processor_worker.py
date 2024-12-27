from dsp_processor import DSPProcessor
from loop import Loop

def run_dsp_process(audio_level, loop_delta, shutdown_event):
    dsp_processor = DSPProcessor()
    loop = Loop(mode="avg", avg_interval=2.0)
    try:
        dsp_processor.start()  # Start the audio stream
        while not shutdown_event.is_set():
            loop.update()
            dsp_processor.update()
            audio_level.value = dsp_processor.level
            loop_delta.value = loop.delta
            loop.print_fps()
    finally:
        try:
            dsp_processor.stop()  # Stop the audio stream
        except:
            pass