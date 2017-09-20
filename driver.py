import XMLProcessor as xml
import DataConnector as cnn
import WeiboFeatureConstructor as wfc
import Segment as seg


# parse wikipedia xml
def parseXml():
    parser = xml.get_parser()
    handler = xml.WikiHandler(cnn.WikiConnector())
    parser.setContentHandler(handler)
    try:
        # parser.parse("data/zhwiki-latest-abstract-zh-cn1.xml")
        # parser.parse("data/zhwiki-latest-abstract-zh-cn2.xml")
        # parser.parse("data/zhwiki-latest-abstract-zh-cn3.xml")
        parser.parse("data/zhwiki-latest-abstract-zh-cn4.xml")
    except xml.TestOverError:
        print("stop")


def construct_weibo_feature():
    constructor = wfc.WeiboFeatureConstructor(cnn.WeiboConnector(), cnn.WikiConnector(), seg.Segment())
    constructor.get_weibo_text_mock()


construct_weibo_feature()
# parseXml()