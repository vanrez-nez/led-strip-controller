import time
from effect_manager import EffectManager

def run_strip_process(audio_level, loop_delta, effect_manager, channel, shutdown_event):
    # Set up event handlers
    def handle_preview(params):
        effect_manager.set_current(params)

    def handle_apply_config(params):
        effect_manager.set_config(params)

    def handle_get_effects(_):
        effects = effect_manager.list_effects()
        channel.respond(effects)

    # Register handlers
    channel.on('preview', handle_preview)
    channel.on('apply_config', handle_apply_config)
    channel.on('get_effects', handle_get_effects)

    try:
        while not shutdown_event.is_set():
            time.sleep(0.001)
            channel.process_events()
            effect_manager.update(loop_delta.value, audio_level.value)
    finally:
        # Cleanup when exiting
        try:
            effect_manager.clear()
        except:
            pass
