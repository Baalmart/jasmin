import unittest, binascii, StringIO
from jasmin.vendor.smpp.pdu.sm_encoding import SMStringEncoder
from jasmin.vendor.smpp.pdu.pdu_types import *
from jasmin.vendor.smpp.pdu.gsm_types import *
from jasmin.vendor.smpp.pdu.pdu_encoding import PDUEncoder

class PDUDecoderTest(unittest.TestCase):

    def getPDU(self, hexStr):
        return PDUEncoder().decode(StringIO.StringIO(binascii.a2b_hex(hexStr)))

    def test_deliver_sm_unknown_param_network_error_code(self):
        pduHex = '000000e40000000500000000542e0f21312e303030000101323434393335353535300005005a4150000400000000000000008069643a3661336564393861363634343465386162616333616364396262613836353666207375623a30303120646c7672643a303030207375626d697420646174653a31343130313630303336353020646f6e6520646174653a31343130313630303338303020737461743a554e44454c4956206572723a30303020746578743a042300033030300427000105001e0021366133656439386136363434346538616261633361636439626261383635366600'
        pdu = self.getPDU(pduHex)
        SMStringEncoder().decodeSM(pdu)

        # Asserts
        self.assertEquals('000', pdu.params['network_error_code'])

    def test_any_network_type(self):
        "Related to #120"

        pduHex = '0000004500000005000000000000000100020135393232393631383600040933373435320000000000000000000000000e00010100060001010424000848692066696b7279'
        pdu = self.getPDU(pduHex)
        SMStringEncoder().decodeSM(pdu)

        # Asserts
        self.assertEquals('GSM', str(pdu.params['source_network_type']))
        self.assertEquals('GSM', str(pdu.params['dest_network_type']))

    def test_any_network_error_code(self):
        "Related to #117"

        pduHex = '000000f3000000050000000000000001000101343931353235363739343838370001013034303531333036393939000400000000000000008569643a62633539623861612d326664322d343033352d383131332d313933303165303530303739207375623a30303120646c7672643a303031207375626d697420646174653a31353035303831343430353820646f6e6520646174653a31353035303831343430353820737461743a44454c49565244206572723a30303020746578743a2d042300030300000427000102001e002562633539623861612d326664322d343033352d383131332d31393330316530353030373900'
        pdu = self.getPDU(pduHex)
        SMStringEncoder().decodeSM(pdu)

        # Asserts
        self.assertEquals('\x03\x00\x00', str(pdu.params['network_error_code']))

    def test_deliver_sm_with_message_payload(self):
        pduHex = '0000009200000005000000000001693c00000032313635333532303730330000003737383800040000000001000000000424004f69643a30303030343336393439207375626d697420646174653a3135303432313135303820646f6e6520646174653a3135303432313135303820737461743a44454c49565244206572723a30303000001e00063661616435000427000102'
        pdu = self.getPDU(pduHex)
        SMStringEncoder().decodeSM(pdu)

        # Asserts
        self.assertEquals('id:0000436949 submit date:1504211508 done date:1504211508 stat:DELIVRD err:000\x00', str(pdu.params['message_payload']))
        self.assertEquals('6aad5', str(pdu.params['receipted_message_id']))

    def test_invalid_command_length(self):
        "Related to #124"

        pduHex = '0000001180000009000000530000000100'
        pdu = self.getPDU(pduHex)

        # Asserts
        self.assertEquals('bind_transceiver_resp', str(pdu.id))
        self.assertEquals('1', str(pdu.seqNum))
        self.assertEquals('ESME_RINVSYSTYP', str(pdu.status))

    def test_invalid_command_length_2(self):
        "Related to #128"

        pduHex = '00000019800000040000000a00000002303030303030303000'
        pdu = self.getPDU(pduHex)

        # Asserts
        self.assertEquals('submit_sm_resp', str(pdu.id))
        self.assertEquals('2', str(pdu.seqNum))
        self.assertEquals('ESME_RINVSRCADR', str(pdu.status))