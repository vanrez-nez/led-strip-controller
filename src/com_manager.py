from base.esp32_uart import UARTCommunication
import os

class ComManager:
  def __init__(self, effectManager):
    self.state = { 'fps': 0 }
    self.effectManager = effectManager
    self.uart = UARTCommunication()
    self.uart.on('state', self.onState)
    self.uart.on('shutdown', self.onState)
    self.uart.on('restart', self.onRestart)
    self.uart.on('preview', self.onPreview)
    self.uart.on('apply_config', self.onApplyConfig)
    self.uart.on("effects_list", self.onEffectsList)

  def onShutdown(self, params):
    print('Shutdown Command')
    os.system('sudo poweroff')

  def onRestart(self, params):
    print('Restart Command')
    os.system('sudo reboot')

  def onApplyConfig(self, params):
    print(params)
    self.effectManager.set_config(params)

  def onPreview(self, params):
    print("Preview: " + params)
    self.effectManager.set_current(params)

  def onEffectsList(self, params):
    sfxList = self.effectManager.list_effects()
    self.uart.send("effects_list", {"effects": sfxList})

  def onState(self, params):
    print('State Command')
    self.uart.send("state", params)

  def update(self, fps):
    self.state['fps'] = fps
    self.uart.update()
