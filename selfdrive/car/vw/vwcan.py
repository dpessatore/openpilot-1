import crcmod
from selfdrive.car.vw.values import CAR, DBC

vw_checksum = crcmod.mkCrcFun(0x12F, initCrc=0xEF, rev=False, xorOut=0xFF)

def create_steering_control(packer, bus, car_fingerprint, steer, idx, lkas_enabled, right):
  values = {
    "CRC": 0x00,
    "Counter": idx,
    "3": 3,
    "Steer_Torque": steer,
    "LKAS_ON": lkas_enabled,
    "_LKAS_Boost": right,
    "1": 1,
    "Torque_Not_0": 1 if steer != 0 else 0,
    "254": 254,
    "7": 7,
  }
  dat = packer.make_can_msg("LKAS", 0, values)[2]
  checksum = vw_checksum(dat)
  values["CRC"] = checksum
  return packer.make_can_msg("LKAS", 0, values)
