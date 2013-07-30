#IOS Translation Tool
##介绍
```
  当IOS项目国际化的时候，手工去翻译每一个字符串是一件非常痛苦的事情。尤其是当项目中存在N多种语言。而且又很难保证，手工翻译的准确性。所以写了一个Python的翻译脚本来做这个事情。
```
##使用说明
```
1、在setting.ini中进行配置。
	NEEDTRANSLATION 为要翻译的语种
	SOURCESPATH	为项目源文件目录
	en… 为具体翻译语种的配置。aim是翻译好的文件的目标路径， dic是字典文件路径，needtr是还需要翻译的字符串输出路径。
2、python translate.py -s setting.ini
```
