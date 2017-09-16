import XMLProcessor as xml
import DataConnector as cnn
import WeiboFeatureConstructor as wfc


# parse wikipedia xml
def parseXml():
    parser = xml.get_parser()
    handler = xml.WikiHandler(cnn.WikiConnector())
    parser.setContentHandler(handler)
    try:
        parser.parse("data/zhwiki-latest-abstract-zh-cn1.xml")
    except xml.TestOverError:
        print("stop")


def construct_weibo_feature():
    constructor = wfc.WeiboFeatureConstructor(cnn.WeiboConnector(), None)
    constructor.getWeiboText()


construct_weibo_feature()