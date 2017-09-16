import XMLProcessor as xml
import DataConnector as cnn
# parse wikipedia xml
parser = xml.get_parser()
handler = xml.WikiHandler(cnn.WikiConnector())
parser.setContentHandler(handler)
try:
    parser.parse("data/zhwiki-latest-abstract-zh-cn1.xml")
except xml.TestOverError:
    print("stop")
