from base.esp32_uart import UARTCommunication
import os
import time

class ComManager:
  def __init__(self, effect_managers, channels=None):
    self.state = { 'fps': 0 }
    self.effect_managers = effect_managers
    self.channels = channels or []
    self.uart = UARTCommunication()
    self.uart.on('state', self.on_state)
    self.uart.on('shutdown', self.on_shutdown)
    self.uart.on('restart', self.on_restart)
    self.uart.on('preview', self.on_preview)
    self.uart.on('apply_config', self.on_apply_config)
    self.uart.on("effects_list", self.on_effects_list)

  def on_shutdown(self, params):
    print('Shutdown Command')
    os.system('sudo poweroff')

  def on_restart(self, params):
    print('Restart Command')
    os.system('sudo reboot')

  def on_apply_config(self, params):
    # Send config to each process
    for channel in self.channels:
      channel.send('apply_config', params)

  def on_preview(self, params):
    print("Preview: " + params)
    # Send preview to each process
    for channel in self.channels:
      channel.send('preview', params)

  def on_effects_list(self, params):
    fx_list = []
    # Request effects list from each process
    for channel in self.channels:
      channel.send('get_effects')

    # Give some time for processes to respond
    time.sleep(0.1)

    # Collect responses
    for channel in self.channels:
      effects = channel.receive()
      if effects:
        # dedup fx_list by name
        effects = [fx for fx in effects if fx['name'] not in [fx['name'] for fx in fx_list]]
        fx_list.extend(effects)

    self.uart.send("effects_list", {"effects": fx_list})

  def on_state(self, params):
    print('State Command')
    self.uart.send("state", params)

  def update(self, fps):
    self.state['fps'] = fps
    self.uart.update()
