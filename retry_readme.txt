class FileFormatVersion:
        byte_value, _ = decode(data, slc.start)
        if isinstance(byte_value, Boolean):
            return CatchX690Boolean(byte_value)



class Meta_cp2(Type[Union[senderType, MeasFileFooter, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[senderType, MeasFileFooter, CatchMetaError]:
        # Decode SenderType or MeasFileFooter
        # sender_type = b''
        # MeasFileFooter = TimeStamp

        # print(item)
        # >> VendorName(vendorName(value='Ericsson'))
        # WHY????
        # print(data[slc])
        # >> b''


  File "/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/env/lib/python3.9/site-packages/x690/types.py", line 221, in value
    return self.decode_raw(self.raw_bytes, self.bounds)
  File "/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/retry.py", line 118, in decode_raw
    err, _ = decode(data, slc.start) # This reads VendorName
  File "/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/env/lib/python3.9/site-packages/x690/types.py", line 161, in decode
    data_slice, next_tlv = get_value_slice(data, start_index)
  File "/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/env/lib/python3.9/site-packages/x690/util.py", line 207, in get_value_slice
    raise X690Error(
x690.exc.X690Error: Invalid Slice slice(5501046, 5501094, None) (data length=5501059)


cleaning:
class Meta_cp2(Type[Union[senderType, MeasFileFooter, CatchMetaError]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.PRIMITIVE]
    TAG = 2

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[senderType, MeasFileFooter, CatchMetaError]:
        #err, _ = decode(data, slc.start) # This reads VendorName
        err = "err"
        item = data[slc]
        try:
            # Please see retry_readme
            if item == b'':
                return senderType("1")
            if len(item) >= 15:
                date_string = data[slc].decode("ascii")
                time_wrapped = datetime.strptime((date_string[0:14]), "%Y%m%d%H%M%S")
                tzone_wrapped = date_string[14-len(date_string):]
                return MeasFileFooter(time_wrapped, tzone_wrapped)
        except:
            return CatchMetaError(err)
        return CatchMetaError(err) #<--- somehow ErrorLens thinks the except block won't be executed if try: fails




After implementing C, C, 3

 File "/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/retry.py", line 218, in decode_raw
    items, _ = decode(data, slc.start, enforce_type=Sequence) # Sequence([Meta_cc0('len(items) != 5'), Data("")])
  File "/home/fieseler/Documents/htwsaar/thesis/Implementation/keavem/env/lib/python3.9/site-packages/x690/types.py", line 167, in decode
    raise UnexpectedType(
x690.exc.UnexpectedType: Unexpected decode result. Expected instance of type <class 'x690.types.Sequence'> but got <class 'retry.FileFormatVersion'> instead


class Data(Type[Union[MeasData, MeasInfo, str]]):
    TYPECLASS = TypeClass.CONTEXT
    NATURE = [TypeNature.CONSTRUCTED]
    TAG = 1

    @staticmethod
    def decode_raw(data: bytes, slc: slice) -> Union[MeasData, MeasInfo, str]:
        items, _ = decode(data, slc.start) # Sequence([Meta_cc0('len(items) != 5'), Data("")])
        if (type(items) == FileFormatVersion):
            return "wtf just happened"

Sequence with 4 items:
⁃ FileFormatVersion(fileFormatVersion(value=260592374909407201031204093729714266))
⁃ SenderName(CatchMetaErrorStr(item='Slice fail'))
⁃ Types(['IPSENTKBYTES', 'IPRECKBYTES', 'IPLOSTPACKUL', 'IPNUMSCAN', 'IPULRECPACK', 'IPDLSENTPACK', 'DL7075STNLOAD', 'DL7680STNLOAD', 'DL8185STNLOAD', 'DL8690STNLOAD', 'DL9195STNLOAD', 'DL9600STNLOAD', 'UL7075STNLOAD', 'UL7680STNLOAD', 'UL8185STNLOAD', 'UL8690STNLOAD', 'UL9195STNLOAD', 'UL9600STNLOAD', 'DL100STNLOAD', 'UL100STNLOAD', 'IPOVLL1', 'IPOVLL2', 'PSDISCOVL', 'CSDISCOVL', 'IPOVLCSREG', 'IPOVLPSREG'])
⁃ Values(None)
Sequence with 3 items:
⁃ FileFormatVersion(fileFormatVersion(value=1323608376056071840644736083242289))
⁃ Data('wtf just happened')
⁃ Meta_cp2(CatchMetaErrorBytes(item=b'\x00'))

Assuming, that:
    ⁃ FileFormatVersion => measObjInstId
    ⁃ Data('wtf just happened') => measResults
    ⁃ Meta_cp2(CatchMetaErrorBytes(item=b'\x00')) => suspectFlag
