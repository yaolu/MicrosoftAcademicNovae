##数据说明
 - AuId_AuId.txt 每一行代表一篇文章的作者的id列表，第一列是文章id，之后是文章所有的作者id
 - all_author.txt 截止到2005年的cs领域所有作者的列表
 - ncols.txt 作者之间和合作关系的适合igraph读取的edge对
 - AuId_Academic_net.txt 第一列为作者id，第二列为文章id，第三列为该文章截止到2005年的引用数，第四到第七列为会议或者期刊的id和名字
 - AuId_CC_Y.txt 截止到2016年，引用数大于5000的作者id，引用数，首次发表文章年份
 - top_conf_journal.txt 顶级会议和顶级期刊的名字以及对应的id，共265个
 - 文件夹 cs_top_conf_journal 顶级会议和顶级期刊的全程和简称，取自微软学术的会议和期刊排名前150名