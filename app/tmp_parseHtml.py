from bs4 import BeautifulSoup

####################################行为

bigTest = [
    '婴儿仰卧，主试者面向婴儿站立，对婴儿微笑、说话，直到婴儿注视到主试者的脸。这时主试者轻轻握住婴儿双肩( 四指并拢置于肩胛骨外侧，食指不能触碰颈部)，将婴儿拉坐起来，观察婴儿控制头的能力',
    '婴儿俯卧，前臂屈曲支撑，用玩具逗引婴儿抬头，观察其反应.',
    '婴儿仰卧，主试者将拇指置于婴儿掌心，余四指握住腕部轻拉婴儿坐起，观察婴儿控制头部的能力',
    '婴儿俯卧，前臂屈曲支撑，用玩具逗引婴儿抬头，观察其反应',
    '竖抱婴儿，观察婴儿控制头部的能力',
    '婴儿俯卧，前臂屈曲支撑，头正中位，用玩具逗引婴儿抬头，观察其反应',
    '主试者扶婴儿腋下，置于立位后放松手的支持，观察其反应',
    '婴儿俯卧，前臂屈曲支撑，头正中位，用玩具逗引婴儿抬头，观察其反应',
    '婴儿仰卧，主试者握住腕部，轻拉到坐的位置',
    '将婴儿以坐姿置于床上',
    '婴儿仰卧，用玩具逗引其翻身',
    '抱坐，主试者示范拍打桌面，鼓励婴儿照样做',
    '扶腋下使婴儿呈悬空位，足离床面20cm~30cm，立位瞬时落下，观察脚落地瞬时的姿势',
    '将婴儿以坐姿置于床上',
    '将婴儿置于床上，协助婴儿双手抓握栏杆，胸部不靠栏杆，呈站立姿势观察',
    '婴儿坐位，用玩具逗引，婴儿.上身可自由转动取物，或轻轻将婴儿肩头向对侧推，观察其侧平衡',
    '站立位，主试者牵婴儿双手，牵手时不过多给力，鼓励婴儿向前行走',
    '婴儿俯卧，用玩具逗引婴儿爬',
    '主试者站立在床或桌边，由婴儿背后扶持其腋下抱起，然后快速做俯冲动作，观察婴儿反应',
    '将婴儿置于俯卧位，用玩具逗引，观察婴儿能否坐起',
    '将婴儿置于立位，待婴儿站稳后松开双手，观察其站立情况',
    '婴儿手扶围栏站立，不得倚靠。将玩具放在其脚边，鼓励婴儿下蹲取物',
    '将小儿置于立位，待小儿站稳后松开双手，观察其站立情况',
    '主试者牵小儿一只手行走，不要用力，观察其行走情况',
    '观察小儿走路的情况',
    '主试者示范过肩扔球，鼓励小儿照样做',
    '主试者示范用脚尖行走，鼓励小儿照样做',
    '在楼梯上放一玩具，鼓励小儿上楼去取',
    '主试者示范双足同时离地跳起，鼓励小儿照样做',
    '鼓励小儿不扶扶手上楼梯，可示范',
    '鼓励小儿不扶扶手下楼梯，可示范',
    '主试者示范用独脚站立，鼓励小儿照样做',
    '主试者示范跳过16开白纸(20cm宽)，鼓励小儿照样做',
    '主试者示范以高抬腿姿势原地交替跳起，鼓励小儿照样做',
    '主试者示范不扶扶手，双足交替上楼，鼓励小儿照样做',
    '主试者示范站在楼梯末级，双足并拢跳至地面，鼓励小儿照样做',
    '主试者示范用独脚站立，鼓励小儿照样做',
    '主试者示范站在楼梯末级，双足并拢跳至地面，鼓励小儿照样做',
    '主试者示范用独脚站立，鼓励小儿照样做',
    '主试者示范，脚跟对脚尖向前走直线，鼓励小儿照样做',
    '主试者示范原地单脚跳，鼓励小儿照样做',
    '主试者示范在一级台阶上以同一只脚上下台阶，鼓励小儿照样做',
    '主试者示范用双手而非前胸接球，然后与小儿相距一米，将球拍给小儿，鼓励小儿用手接住球',
    '主试者示范，脚跟对脚尖向后走直线，鼓励小儿照样做',
    '主试者示范原地抱肘单脚跳，鼓励小儿照样做',
    '主试者示范拍球，鼓励小儿照样做(向下扔落地的第一下不算拍球)。允许试三次',
    '主试者示范用一手提绳，将球停稳，以内踝及足弓内侧来踢球，鼓励小儿照样做。如小儿用足外侧踢，可示范更正一次姿势',
    '主试者示范拍球，鼓励小儿照样做( 向下扔落地的第一下不算拍球)。允许试三次',
    '主试者示范用一手提绳，将球停稳，以内踝及足弓内侧来踢球，鼓励小儿照样做。如小儿用足外侧踢，可示范更正一次姿势',
    '主试者示范在一级台阶上交替换脚上下共3组(示范时主试者要边喊口号边示范)，请小儿照样做，若小儿不会两脚交替可提醒小儿“换脚”',
]
bigResult = [
    '婴儿头可竖直保持2s或以上',
    '婴儿有头部翘动即可通过',
    '当把婴儿拉起成坐位时婴儿头可自行竖直,保持5s或以上',
    '婴儿可自行将头抬离床面达2s或以上。',
    '能将头举正并稳定10s或以上',
    '头可自行抬离床面，面部与床面成45°，持续5s或以上',
    '婴儿可用自己双腿支持大部分体重达2s或以上',
    '头可自行抬离床面，面部与床面呈90°，持续5s或以上',
    '婴儿自己能主动用力坐起，拉坐过程中无头部后滞现象',
    '独坐保持5s或以上,头身向前倾',
    '观察或询问，婴儿可从仰卧自行翻到俯卧位',
    '婴儿经示范后或自发拍打桌面，并拍响',
    '婴儿能全脚掌着地',
    '独坐时背直，无需手支撑床面，保持1min或以上',
    '双手扶栏杆支撑全身重量，保持站立位5s或以上',
    '独坐时无须手支撑，上身可自由转动取物或侧推后回正保持平衡不倒',
    '婴儿可自己用力,较协调地移动双腿，向前行走三步或以上',
    '婴儿能将腹部抬离床面，四点支撑向前爬行(膝手爬)',
    '婴儿出现双手张开，向前伸臂，类似保护自己的动作',
    '无需协助，婴儿能较协调地从俯卧位坐起，并坐稳',
    '婴儿能独自站立2s或以上一手扶栏杆蹲下，用另一只手',
    '捡玩具，并能再站起来',
    '独自站立10s或以上，允许身体轻微晃动',
    '小儿自己迈步，牵一手能协调地移动双腿，至少向前迈三步以上',
    '小儿行走自如，不左右摇摆，会控制步速，不惯性前冲',
    '小儿举手过肩扔球，可无方向',
    '小儿能用脚尖连续行走三步以上，脚跟不得着地',
    '小儿能扶楼梯扶手，熟练地上三阶以上台阶。',
    '小儿会双足同时跳离地面，同时落地，两次以上',
    '不扶扶手，稳定地上楼梯三阶或以上',
    '不扶扶手，稳定地下楼梯三阶或以上',
    '小儿不扶任何物体可单脚站立2s或以上',
    '小儿双足同时离地跳起跃过纸，不得踩到纸',
    '小儿可双足交替跳起,双脚离地5cm',
    '小儿上台阶交替用脚，一步一台阶，可交替上楼三阶或以上',
    '小儿双足并拢跳至地面，双足落地后两脚间距离小于10cm',
    '小儿独脚站立5s或以上,身体稳定',
    '小儿双足并拢跳至地面，双足落地后两脚间距离小于5cm,并站稳',
    '小儿独脚站立10s或以上，身体稳定',
    '小儿能脚跟对脚尖向前走2m(六步)，允许身体有小幅晃动',
    '小儿能单脚连续跳3次或以上，可伸开双臂保持平衡，允许小儿在一脚范围内跳动',
    '小儿以同一只脚能稳当并较熟练地完成3组，可稍有停顿',
    '小儿用手接住球，三次中接住一次即可，用双臂或用前胸接球不通过',
    '小儿能脚跟对脚尖向后走2m(六步)，允许身体有小幅晃动',
    '小儿抱肘单脚原地连续跳3次或以上，基本在原地跳动',
    '小儿连续拍球2个或以上',
    '小儿连续用足内踝踢球2个或以上',
    '小儿连续拍球5个或以上',
    '小儿用足内踝踢球3个或以上，踢一下落地一下',
    '小儿能稳当并较熟练地两脚交替完成3组，可稍有停顿',
]
fineTest = [
    '婴儿仰卧，主试者将食指从尺侧放入婴儿手掌中',
    '主试者观察婴儿清醒时手的自然状态',
    '婴儿仰卧，将花铃棒放在婴儿手中',
    '主试者分别轻叩婴儿双手手背，观察拇指自然放松的状态',
    '婴儿仰卧或侧卧，将花铃棒放入婴儿手中',
    '婴儿仰卧，主试者观察婴儿双手是否能够自发搭在一起，或主试者将其两手搭在一一起，随即松手，观察婴儿双手状态。',
    '抱坐，将花铃棒放入婴儿手中，鼓励婴儿摇动',
    '婴儿仰卧，将花铃棒拿到婴儿可及的范围内，观察婴儿反应，但不能触碰婴儿',
    '抱坐，婴儿手置于桌上。玩具(如花铃棒)放在距离婴儿手掌一侧2.5cm处，鼓励婴儿取玩具',
    '观察婴儿能否把双手放在一起互相玩弄',
    '将一张28g粉色打字纸放入婴儿手中，使婴儿能抓住纸，观察婴儿反应',
    '抱坐，放一积木在婴儿容易够到的桌面上，观察婴儿反应',
    '抱坐，将一小丸放在桌上，鼓励婴儿取',
    '抱坐，出示一积木给婴儿，抓住后，再出示另一块，观察其反应',
    '抱坐，将一小丸放在桌上，鼓励婴儿取',
    '连续出示两块积木后婴儿均能拿到，再出示第三块积木鼓励婴儿取',
    '抱坐，将一小丸放在桌上，鼓励婴儿取',
    '主试者在婴儿注视下将积木放入杯中，鼓励婴儿取出',
    '抱坐，将一小丸放在桌上，鼓励婴儿取',
    '主试者示范将积木放入杯中，鼓励婴儿照样做',
    '主试者示范用笔在纸上画道，鼓励小儿模仿',
    '出示一小丸及30ml广口试剂瓶，主试者拿瓶，示范并指点将小丸放入瓶内，鼓励小儿照样做',
    '主试者出示纸和笔，鼓励小儿画画',
    '出示装有小丸的30ml广口试剂瓶，递给小儿，说“阿姨想要豆豆(小丸)怎么办?”或“把豆豆给妈妈”。鼓励小儿将小丸取出，但不能说倒出',
    '主试者示范用蜡笔画出-无方向道道，鼓励小儿模仿',
    '主试者示范用水晶线穿过扣眼，鼓励小儿照样做',
    '示范拉拉锁，拉上、拉下各一次。主试者固定拉锁两端，鼓励小儿照样做',
    '主试者示范用水晶线穿过扣眼，并将线拉出，鼓励小儿照样做',
    '主试者与小儿同向，示范画一垂直线，注意测查纸张放正，鼓励小儿模仿',
    '出示打开的拉锁，示范将拉锁对好，鼓励小儿照样做',
    '主试者示范连续穿扣3~5个，鼓励小儿照样做',
    '示范用下面二块，上面一块共三块积木搭成有孔的桥，并保留模型，鼓励小儿照样做。主试者不得提示桥孔',
    '主试者示范画一圆形，鼓励小儿模仿',
    '出示打开的拉锁，示范将拉锁对好并拉上，鼓励小儿照样做',
    '主试者与小儿同向示范画交叉线，鼓励小儿模仿',
    '主试者出示螺丝、螺母，嘱其拧上。如小儿不会，可示范',
    '主试者让小儿用4块塑料板拼圆形，用2块等边三角形板拼正方形，共限时2min',
    '主试者示范用打印纸剪一-直线，鼓励小儿照样做',
    '主试者示范画一正方形，鼓励小儿模仿',
    '主试者出示组装好的螺丝图片5s后收起，将分开的螺丝、平垫和螺母交给小儿，请小儿凭记忆组装。主试者可针对落下的零件提示“还有呢?”',
    '主试者示范用一长方形纸横竖对齐各折一次，鼓励小儿照样做',
    '主试者鼓励小儿用筷子夹花生米，从桌子上夹到盒子里，连做三遍',
    '将事先画好的椭圆形放在小儿面前，瞩其将6块塑料片按图分别放进去，不予提醒，限时2min',
    '主试者给小儿出示一张已画好圆形(直径7.5cm米)的1/2A4打印纸，鼓励小儿将圆形剪下(附原图)',
    '主试者让小儿写出自己的名字',
    '主试者给小儿出示一张已画好圆形(直径7.5cm)的1/2A4打印纸，鼓励小儿将圆形剪下(附原图)',
    '主试者让小儿用2块非等边三角形板拼长方形，出示时要求短边相对，限时2min',
    '主试者出示正方形和圆形的组合图形，鼓励小儿临摹。',
    '主试者出示六边形图形，鼓励小儿临摹',
    '出示一双筷子和一根绳，主试者示范用绳将筷子以活结方式捆上，鼓励小儿照样做。小儿打结时主试者应辅助固定筷子',
    '主试者示范将一根绳子做翻绳最初级模式，鼓励小儿跟着做',
    '出示一双筷子和一根绳，鼓励其用绳将筷子以活结方式捆上，小儿打结时主试者应辅助固定筷子',
]
fineResult = [
    '婴儿能将拳头握紧',
    '双手拇指内收不达掌心，无发紧即通过',
    '握住花铃棒不松手达2s或以上',
    '婴儿双手握拳稍紧，拇指稍内收，但经轻叩即可打开',
    '婴儿能握住花铃棒30s，不借助床面的支持',
    '婴儿能将双手搭在一起，保持3s~4s',
    '婴儿能注视花铃棒，并摇动数下',
    '婴儿手臂试图抬起或有手抓.动作即可通过',
    '婴儿可用一手或双手抓住玩具',
    '婴儿会自发将双手抱到一起玩',
    '能用双手反复揉搓纸张两次或以上，或将纸撕破',
    '婴儿伸出手触碰到积木并抓，握到',
    '婴儿用所有手指弯曲做耙弄、搔抓动作,最后成功地用全掌抓到小丸',
    '婴儿主动伸手去抓桌上的积木，第一块积木握住并保留在手中后，又成功地用另一只手抓住第二块积木',
    '婴儿会用拇他指捏起小丸',
    '有要取第三块积木的表现，不一定能取到，前两块仍保留在手中',
    '婴儿会用拇食指捏起小丸',
    '婴儿能自行将积木取出，不能倒出',
    '婴儿会用拇食指的指端协调、熟练且迅速地对捏起小丸',
    '婴儿能有意识地将积木放入杯中并撒开手',
    '小儿握笔在纸上留下笔道即可',
    '小儿捏住小丸试往瓶内投放,但不一定成功',
    '小儿能用笔在纸上自行乱画',
    '小儿能将小丸拿出或倒出',
    '小儿能画出道道，起止自如，方向不限',
    '小儿能将水晶线穿过扣眼0. 5cm以上',
    '小儿能双手配合将锁头来回移动，超过全拉锁的一半',
    '小儿能将水晶线穿过扣眼，并能将线拉出',
    '小儿能画竖线，长度> 2.5cm,所画线与垂直线的夹角应<30°',
    '小儿能将拉锁头部分或全部插进锁孔',
    '小儿能较熟练穿扣并拉过线3个或以上',
    '小儿能搭出有孔的桥',
    '小儿所画圆二头相交，为闭合圆形，不能明显成角',
    '小儿能将拉锁头全部插进锁孔，并有拉的意识',
    '小儿能画出两直线并相交成角，直线线条较连续',
    '小儿能双手配合将螺丝、螺母组装起来',
    '两个图形均要拼对',
    '小儿能够剪出直线，长度大于10cm，与主剪方向角度小于15°',
    '小儿能基本模仿画出，所画图形允许稍有倾斜，有一个角可以<45°',
    '小儿无需提示或稍经提示后自行将螺丝、平垫、螺母按顺序组装起来',
    '小儿折纸基本成长方形，折纸边差距<1cm，纸边夹角<15°',
    '小儿熟练地夹起三次以上,过程中无掉落',
    '小儿全部拼对',
    '小儿能剪出大致圆形，允许出角',
    '小儿能正确写出自己的名字。',
    '小儿能剪出平滑的圆形，无成角、毛边',
    '小儿拼对长方形',
    '小儿能画出，无转向',
    '小儿可临摹出六边形，6个角均画得好，连接线平直',
    '经示范后，小儿能用活结将筷子捆上',
    '小儿能跟着主试者一步一步，或在主试者示范后自行做到中指挑绳',
    '无需示范，小儿能用活结将筷子捆上',
]
adaptTest = [
    '婴儿仰卧，主试者将黑白靶拿在距婴儿脸部上方20cm处移动，吸引婴儿注意',
    '婴儿仰卧，主试者手提红球，在婴儿脸部上方20cm处轻轻晃动以引起婴儿注意，然后把红球慢慢移动，从头的一侧沿着弧形，移向中央，再移向头的另一侧，观察婴.儿头部和眼睛的活动。',
    '婴儿仰卧，用娃娃在婴儿脸部上方20cm处晃动，观察其反应。',
    '婴儿仰卧，主试者提起红球，在婴儿脸部上方20cm处轻轻晃动以引起婴儿注意，先慢慢向上移动，然后再从头顶向下颏处移动',
    '婴儿仰卧，主试者将娃娃在婴儿身体上方20cm处沿中线自下向上移动。当玩具到婴儿乳头连线至下颏之间时，观察婴儿反应',
    '婴儿仰卧，主试者手提红球，在婴儿脸部上方20cm处轻轻晃动以引起婴儿注意,然后把红球慢慢移动,从头的一侧沿着弧形，移向中央，再移向头的另一侧，观察婴儿头部和眼睛的活动',
    '主试者或母亲对婴儿说话，观察婴儿是否与人对视',
    '观察或询问婴儿在高兴或不满时的发音',
    '桌面上放一小丸，主试者指点小丸或把小丸动来动去,以引起婴儿注意',
    '抱坐，婴儿手置于桌上，主试者先放一块积木在婴儿手中，再放另一块积木于桌上婴儿可及范围内，适当逗引，观察婴儿对第二块积木的反应.',
    '抱坐，先后递给婴儿两块积木，婴儿自己拿或被动放在手中均可',
    '以红球逗引婴儿注意，红球位置应与婴儿双眼在同一水平线上。主试者手提红球，当婴儿注意到红球后，立即松手使红球落地，此时主试者的手保持原姿势，观察婴儿反应',
    '抱坐，出示一积木给婴儿，婴儿拿住后，再向拿积木的手前出示另一块积木，观察其反应',
    '抱坐，将一玩具放于婴儿手恰好够不到的桌面上，观察其反应',
    '主试者示范摇铃，鼓励婴儿照样做',
    '以玩具逗引婴儿来取，将要取到时，主试者将玩具移动到稍远的地方，观察其反应',
    '主试者出示两块积木，示范积木对敲后，让婴儿一手拿一块，鼓励其照样做',
    '主试者轻摇铜铃以引起婴儿注意，然后将铜铃递给婴儿，观察其对铜铃的反应',
    '积木放在桌上，在婴儿注视下用杯子盖住积木，杯子的把手对着婴儿，鼓励婴儿取积木',
    '在婴儿面前摇响装有硬币的盒，然后避开婴儿将硬币取出，给婴儿空盒，观察其反应',
    '在婴儿注视下用方巾包起一积木，然后打开，再包上，鼓励婴儿找',
    '主试者示范拍娃娃，鼓励婴儿照样做',
    '瓶盖翻放在桌上，主试者示范将瓶盖盖在瓶上，鼓励小儿照样做',
    '主试者示范翻书，鼓励小儿照样做',
    '试者示范将圆盒盖好，鼓励小儿照样做',
    '示范搭高两块积木，推倒后一块一块出示积木，鼓励小儿搭高',
    '在型板圆孔下方放一圆积木，圆孔靠近小儿身体。主试者对小儿说“这是小朋友的家(指型板面而不是圆孔) ,请帮这个小朋友(指圆积木)找到自己的家”，不示范',
    '示范搭高两块积木，推倒后一块一块出示积木，鼓励小儿搭高',
    '出示红、黄、蓝、绿四色图片，问小儿“哪个是红色?”',
    '主试者示范一页页翻书，鼓励小儿照样做',
    '在小儿能正放圆积木入型板的基础上，将型板倒转180°。圆积木仍在原处，主试者对小儿说“这是小朋友的家(指型板)，请帮这个小朋友(指圆积木)找到自己的家”，不示范',
    '主试者向小儿出示大小圆片，请小儿把大的给妈妈或阿姨',
    '将圆、方、三角形三块积木放在与型板相应的孔旁，主试者对小儿说“这是小朋友的家(指型板)，请帮这些小朋友(指三块积木)找到自己的家”，不示范。放置三角型积木方向要与型板一致',
    '一块和数块积木分放两边，请小儿指出哪边是多的，再指另一边问“这是几个?”',
    '在小儿正放三块积木入型板的基础上，将型板倒转180°，三块积木仍在原处，主试者对小儿说“这是小朋友的家(指型板)，请帮这些小朋友(指三块积木)找到自己的家”，不示范',
    '示范搭高二块积木，推倒后一块一块出示积木，鼓励小儿搭高。允许试三次',
    '嘱小儿做三件事擦桌子、摇铃、把门打开，可再重复命令一遍。小儿开始做后，不能再提醒或给予暗示',
    '主试者出示三块积木，问小儿“这是几块?”',
    '出示红、黄、蓝、绿四色图片，先从非红色开始问，避免顺口溜出，请小儿说出各为何种颜色',
    '主试者出示五块积木，问小儿“这是几块?”',
    '主试者出示红、黄、蓝、绿四色图片，先从非红色开始问，避免顺口溜出，请小儿说出各为何种颜色',
    '出示找不同图画，主试者问小儿两张图画有什么不同之处?小熊示教，限时2min',
    '出示补缺图片，主试者问小儿各图中缺什么?第一幅图示教',
    '主试者给小儿一个圆形扣子，然后出示第一组模板(包括圆型、方型、三角型)，问“你手里的东西和我这些东西哪些是一类的?为什么?”然后收起，再出示第二组模版(包括方型钮扣、三角型、方型)，提问同上',
    '出示补缺图片，主试者问小儿各图中缺什么?第一幅图示教',
    '出示找不同图画，主试者问小儿两张图画有什么不同之处?小熊示教。限时2min',
    '出示补缺图片，主试者问小儿各图中缺什么?第一幅图示教',
    '主试者问小儿“两棵树之间站一个人，一排三棵树之间站几个人?”',
    '主试者问小儿“将一个苹果十字切开是几块?”如小儿不理解，主试者可用手势比划提示',
    '出示找不同图画，主试者问小儿两张图画有什么不同之处?小熊示教。限时2min',
    '主试者让小儿用左手摸右耳朵，右手摸左耳朵，右手摸右腿',
    '主试者出示图形，问右边的4幅图中哪一幅放在左边空白处合适。第一题示教',
    '主试者问小儿“面粉能做哪些东西?”',
    '主试者出示图形，问下边的4幅图中哪一幅放在上边空白处合适。第一题示教',
    '主试者问小儿“什么动物没有脚?”(脚定义为走路用的)',
]
adaptResult = [
    '婴儿眼睛可明确注视黑白靶',
    '当主试者把红球移向中央时，婴儿用眼睛跟踪看着红球转过中线，三试一成',
    '可立刻注意到娃娃，三试一成',
    '婴儿眼睛能上或下跟随红球',
    '当娃娃移动至婴儿乳头连线至下颌之间时，立即注意即可通过',
    '婴儿用眼及头跟随红球转动180°，三试一成',
    '婴儿能与成人对视，并保持5s或以上.',
    '会高声叫(非高调尖叫)',
    '婴儿明确地注意到小丸',
    '婴儿拿着放在手中的第一块积木，当第二块积木靠近时，目光明确地注视第二块积木',
    '婴儿一手拿一块积木，保持在手里10s或以上',
    '红球落地后，婴儿立即低下头寻找红球',
    '婴儿将第一块积木传到另一只手后，再去拿第二块积木',
    '欠身取，并能拿到玩具',
    '婴儿能够有意识地摇铃',
    '婴儿持续追逐玩具，力图拿到，但不一定取到',
    '婴儿能把双手合到中线，互敲积木，对击可不十分准确',
    '婴儿有意识寻找并拨弄或拿捏铃舌',
    '婴儿能主动拿掉杯子,取出藏在杯子里面的积木',
    '婴儿能明确地寻找盒内的硬币',
    '婴儿有意识地打开包积木的方巾，寻找积木，成功将积木拿到手',
    '婴儿学大人样子轻拍娃娃',
    '小儿会将瓶盖翻正后盖在瓶上',
    '做出翻书动作两次或以上',
    '小儿会将圆盒盖上，并盖严',
    '小儿搭高四块积木或以上，三试一成',
    '不经指点，能正确将圆积木一次性放入孔内',
    '小儿搭高7~8块积木，三试一成',
    '小儿能在四色图片中正确指出红色',
    '小儿会用手捻书页，每次一页，连续翻书三页或以上',
    '型板倒转后，小儿能正确将圆积木一次性放入圆孔内',
    '小儿会正确把大的给妈妈或阿姨，三试二成',
    '小儿能一次性正确放入相应孔内，仅等腰三角形可提示',
    '小儿先正确指出哪一边多，后回答“是1个”',
    '小儿能一次性正确放入翻转后型板的相应孔内，仅等腰三角形可提示',
    '小儿能搭高积木10块。三试一成',
    '小儿会做每件事情,没有遗忘任何一项，但顺序可颠倒',
    '小儿能正确说出“三块',
    '能正确说出两种或以上颜色',
    '小儿能正确说出“五块”',
    '四种颜色全部答对',
    '能找到包括示教内容的3处不同或以上',
    '要求说对包括示教内容的三幅图或以上',
    '两问均答对',
    '要求说对包括示教内容的四幅图或以上',
    '能找到包括示教内容的5处不同或以上',
    '要求说对包括示教内容的五幅图或以上',
    '小儿回答“两个人。',
    '不经提示或仅在主试者手势比划提示后答“四块',
    '能找到包括示教内容的7处不同或以上',
    '小儿全部做对',
    '小儿能指对包括第一题在内的三道题或以上',
    '小儿能回答两种或以上',
    '小儿能指对包括第一题在内的三道题或以上',
    '小儿回答蛇、鱼等两类或以上没有脚的动物',
]
languageTest = [
    '婴儿仰卧、清醒。注意其发音',
    '婴儿仰卧，在其一侧耳上方10cm~15cm处轻摇铜铃，观察婴儿的反应。(双侧均做，一侧通过即可)',
    '询问或逗引婴儿发音',
    '婴儿仰卧，在其一侧耳上方10cm~15cm处轻摇铜铃，观察婴儿的反应。(双侧均做， 一侧通过即可)',
    '逗引婴儿笑，但不得接触身体',
    '观察婴儿安静时的发音',
    '抱坐，主试者在婴儿耳后，上方15cm处轻摇铜铃，观察其反应',
    '观察或询问婴儿看到熟悉的人或玩具时的发音',
    '主试者或家长在婴儿背后呼唤其名字，观察其反应',
    '主试者或妈妈(带养人)伸手表示要抱，不得出声提示，观察婴儿反应',
    '观察婴儿在清醒状态时的发声情况',
    '观察或询问婴儿是否会模仿咳嗽、弄舌的声音',
    '主试者询问家长，婴儿是否常有主动伸手表示要抱:摊开手表示没有:咂咂嘴表示好吃等动作手势',
    '主试者只说欢迎，不做手势示范，鼓励婴儿以手势表示',
    '主试者只说再见，不做手势示范，鼓励婴儿以手势表示',
    '观察或询问婴儿是否会模仿“妈妈”、“爸爸”、“拿”、“走”等语音',
    '观察或询问婴儿有意识的发音情况',
    '婴儿取一玩具玩时，主试者说“不动”、“不拿”， 不要做手势，观察或询问其反应',
    '观察或询问小儿见到妈妈、爸爸时，是否会有意识并准确地叫出',
    '将一玩具放入小儿手中，然后主试者或家长对小儿说“把某某东西给我”，不要伸手去拿，观察小儿反应',
    '主试者问小儿“眼在哪儿?”“耳在哪儿?”“鼻子在哪儿?”等，观察其反应',
    '观察或询问小儿有意识讲话的情况',
    '请小儿把三块积木分别递给妈妈、阿姨、放在桌子上，妈妈阿姨不能伸手要',
    '观察或询问小儿有意识讲话的情况并记录',
    '主试者问“这是什么(球) ?”“那是谁(带小儿者) ?”“爸爸干什么去了(上班) ?”',
    '观察或询问小儿有意识说话的情况',
    '鼓励小儿说唐诗或儿歌',
    '主试者分别提问小儿碗、笔、板凳、球的用途',
    '主试者说一句话“星期天妈妈带我去公园”，可重复一遍，鼓励小儿复述',
    '主试者对小儿说“请举举你的手”和“请抬抬你的脚”,可重复指令一遍，但不能有示范的动作，观察小儿反应',
    '出示图片，依次指给小儿看，鼓励其说出图片名称',
    '主试者问小儿“你叫什么名字?”',
    '主试者问小儿性别，若是女孩问“你是女孩还是男孩?”;若是男孩问“你是男孩还是女孩?”',
    '主试者将一小丸放入30毫升广口试剂瓶内问“小丸是在瓶里?还是在瓶外?”',
    '出示图片，依次指给小儿看，鼓励其说出图片名称',
    '观察小儿在说话时的发音情况',
    '主试者分别问(1) 火是热的，冰呢? (2) 大象的鼻子是长的，小兔的尾巴呢? (3) 头发是黑的，牙齿呢? (4)木头是硬的，棉花呢?',
    '主试者依次出示积木△○口，问小儿“这是什么形状?”',
    '主试者说一句话“妈妈叫我一定不要和小朋友打架”，可重复一遍，鼓励小儿复述',
    '主试者问(1)锅是做什么用的? (2) 手机是干什么用的? (3)眼睛有什么作用?',
    '观察小儿是否会漱口',
    '主试者出示图片，随意指出10以内数字，让小儿认',
    '主试者问小儿“你姓什么?”',
    '主试者让小儿说出两种圆形的东西',
    '主试者问小儿“你是属什么的?',
    '主试者先示教“你会倒着数数吗?1、2、3倒数就....3、2、1,现在请你从21开始倒数，21、23、22、21.....”，鼓励小儿完成倒数',
    '主试者出示三幅连环画，然后对小儿说“这三幅图连起来讲了一个故事，请你给我讲一讲故事的内容是什么?小猴子为什么哭了?”若小儿回答第一问后不再答，可再追问“小猴子为什么哭了?”',
    '主试者问(1)人为什么要上班? ——挣钱或建设国家(2)房子为什么要有窗户? ——透光或通风(3)苹果和香蕉有什么共同点? ——水果',
    '主试者出示三幅连环画，然后对小儿说“这三幅图连起来讲了一个故事，请你给我讲一讲故事的内容是什么?小猴子为什么哭了?”若小儿回答第一问后不再答，可再追问“小猴子为什么哭了?”',
    '主试者请小儿看钟表图辨认时间',
    '主试者问小儿“小朋友为什么要打预防针?”',
    '主试者问小儿“毛衣、长裤和鞋有什么共同之处?”',
]
languageResult = [
    '观察或询问，小儿能发出任何一种细小柔和的喉音',
    '婴儿听到铃声有一种或多种反应',
    '能从喉部发出a、0、e等元音来',
    '婴儿听到声音有表情和肢体动作的变化',
    '观察或询问，婴儿能发出“咯咯” 笑声',
    '观察或询问，婴儿会类似自言自语，无音节、无意义.',
    '可回头找到声源，一侧耳通过即可',
    '观察或询问，婴儿会发出象说话般的声音,如伊伊呀呀、ma、pa、ba等辅元结合音',
    '婴儿会转头寻找呼唤的人',
    '婴儿理解并将手伸向主试者或妈妈(带养人)，二试一成',
    '观察或询问，婴儿会发da-da、ma-ma的双唇音，但无所指',
    '观察或询问，婴儿能模仿发出类似声音',
    '三问中，有两项表现即可通过',
    '观察或询问，婴儿能够做出欢迎的手势',
    '观察或询问，婴儿能够做出再见的手势',
    '观察或询问，婴儿能模仿发语声',
    '观察或询问，有意识并正确地发出相应的字音，如爸、妈、拿、走、姨、奶、汪汪等',
    '观察或询问，婴儿会停止拿取玩具的动作',
    '小儿会主动地称呼爸爸或妈妈',
    '经要求，小儿把玩具主动递给主试者或家长，并主动松手',
    '能正确指出3个或3个以上身体部位',
    '有意识地说3~5个字(妈、爸除外)',
    '小儿会正确地将积木送到要求的地方',
    '有意识说10个或以，上单字或词(爸、妈除外)',
    '小儿均能正确回答',
    '小儿能有意识地说出3~5个字的句子，有主谓语',
    '小儿能自发或稍经提示开头后完整说出两句或以上唐诗或儿歌',
    '小儿会说出三种或以上物品的用途',
    '小儿能复述出7个字及以上, 不影响句意表达',
    '小儿能按指令做出举手或抬脚动作',
    '小儿能正确说出10样及以上。记录1.北极熊2.树叶3.小鸡4.青蛙5.螳螂6.猕猴桃7.树8.房子9.雨伞10.壶11.铅笔12.钥匙13.打印机14.刀15.电脑16.管钳17.轮船18.毛笔和砚台19.国旗20.脚21.嘴唇22.步枪23.雪花21中国结',
    '小儿能正确回答自己的大名',
    '小儿能正确说出自己的性别',
    '小儿会正确说出是在里边',
    '小儿能正确说出14样及以上。记录1.北极熊2.树叶3.小鸡4.青蛙5.螳螂6.猕猴桃7.树8.房子9.雨伞10.壶11.铅笔12. 钥匙13.打印机14.刀15.电脑16.管钳17.轮船18.毛笔和砚台19.国旗20.脚21.嘴唇22.步枪23.雪花21中国结',
    '小儿会发清楚大多数语音，不影响交流',
    '四题中答对两个或以上',
    '小儿能正确回答三个图形的名称',
    '小儿能够复述较完整的复合句，偶尔漏字/错字',
    '三问均正确。',
    '小儿能灵活左右漱口并将水吐出',
    '小儿全部正确答出',
    '小儿正确回答出姓，连名带姓不能通过',
    '小儿能说出两种或以，上圆形的东西',
    '小儿能正确说出自己的属相',
    '小儿能较流利地正确数出13~1',
    '能分别描述每张图画的基本内容',
    '答对两题或以上。(1)挣钱或建设国家; (2) 透光或通风; (3) 水果',
    '能明确理解故事的主题',
    '小儿能辨认两张图或以上所表示的时间',
    '小儿能表达出预防生病/感冒或打预防针可以不生病等',
    '小儿回答都是穿的、能保暖',
]
societyTest = [
    '主试者面对婴儿的脸微笑并对其说话。但不能触碰婴儿的面孔或身体',
    '婴儿横放在床.上或斜躺在家长臂弯里，主试者站立(直立位，勿弯腰)逗引婴儿引起其注意后左右走动，观察婴儿眼睛是否追随主试者',
    '观察或询问婴儿在无外界逗引时是否有自发微笑的情况',
    '婴儿仰卧，主试者弯腰，对婴儿点头微笑或说话进行逗引，观察其反应。但不能触碰婴儿的面孔或身体',
    '主试者面对婴儿，不做出接近性的社交行为或动作，观察婴儿在无人逗引时的表情',
    '主试者观察婴儿在不经逗引的情况下，对周围人和环境的反应',
    '将无边镜子横放在婴儿面前约20cm处，主试者或母亲可在镜中逗引婴儿，观察婴儿反应',
    '观察婴儿在看到母亲或其他亲人或听到亲人声音后的表情变化',
    '将无边镜子竖放在婴儿面前约20cm处，主试者及家长影像不能在镜内出现，观察婴儿反应',
    '观察婴儿看到奶瓶、饼干、水等食物时的反应',
    '观察或询问婴儿拿到一块饼干或其他能拿住的食物时，能否送至口中并咀嚼',
    '主试者把自己的脸藏在--张中心有孔的A4纸后面(孔直径0.5cm)，呼唤婴儿名字，婴儿听到声音，观望时，主试者沿纸边在纸的同一侧反复出现两次并逗引说“喵、喵”，第三次呼唤婴儿名字后从纸孔观察婴儿表情',
    '婴儿仰卧，观察其是否会自发或在主试者协助下将脚放入手中后玩脚',
    '观察或询问婴儿对陌生人的反应',
    '主试者或家长对婴儿训斥或赞许，观察其反应',
    '观察或询问婴儿对不感兴趣的物品的反应',
    '主试者问婴儿“妈妈在哪里? ”“灯在哪里?”“阿姨在哪里?”等人或物的名称，观察其反应',
    '将娃娃、球和杯子并排放在婴儿双手可及的桌面上，鼓励婴儿按指令取其中的- -件。(每样 东西交替问两次，不能连续问)',
    '观察或询问婴儿能否从成人拿的杯子里喝到水',
    '主试者将帽子戴在婴儿头上，观察其能否摘下帽子',
    '观察或询问成人给小儿穿衣时的配合情况',
    '观察或询问，对家长指示的某一场景或过程， 小儿能否与家长一起关注',
    '观察或询问小儿脱袜子的方法',
    '观察或询问小儿大小便控制情况，或询问白天是否尿湿裤子',
    '观察或询问小儿是否会自己用匙',
    '观察或询问小儿是否会明确表示自己的需要',
    '观察或询问小儿是否有想象性游戏，如假装给娃娃或动物玩具喂饭、盖被子、打针等',
    '示范或不示范小儿见人打招呼',
    '观察或询问，小儿在见到某物时，是否能自发提问“这是什么?',
    '观察或询问小儿是否会自己脱上衣或裤子',
    '主试者问小儿“打人对不对?”，观察小儿的反应或回答',
    '在一个无把儿的杯中注入1/3杯水，主试者示范将水倒入另一杯中，来回各倒一次，鼓励小儿照样做',
    '出示图片，问小儿“ 乱扔垃圾是不对的，你看这个小女孩吃完的果皮应该扔哪儿?”，鼓励小儿回答',
    '主试者将小儿鞋脱下，鞋尖对着小儿，鼓励其穿上',
    '出示娃娃，鼓励小儿解扣子，主试者应辅助小儿固定娃娃衣服',
    '主试者依次问“饿了怎么办?冷了怎么办?累了怎么办?”',
    '出示娃娃，鼓励小儿扣扣子，主试者应辅助小儿固定娃娃衣服',
    '观察小儿是否会穿上衣',
    '主试者问小儿“吃饭之前为什么要洗手”?',
    '观察或询问小儿能否做集体游戏',
    '出示男女厕所标识图片，问小儿应该进哪个厕所，并提问“为什么”',
    '如在上午测试，主试者问(1)现在是上午还是下午? (2)太阳落山是在下午还是上午?如在 下午测试，则主试者问(1)现在是下午还是上午? (2) 太阳升起是在上午还是下午?',
    '主试者问小儿一只手有几个手指，如答对，再问两只手有几个手指',
    '主试者问小儿“你家住在哪里?”，或追问“你再说详细些，我怎么送你回家呢?”',
    '主试者问小儿:“过马路为什么要走人行横道?”',
    '出示鸡在水中游图画，主试者问小儿画的对不对，如回答“不对”，问哪里画错了',
    '主试者问小儿一年有哪四个季节',
    '依次出示两组标识图片，问“哪一个是代表危险的标志?为什么?”',
    '主试者先告诉小儿今天是星期几，然后提问“请告诉我后天是星期几?明天是星期几?”',
    '出示雨中看书图片，主试者问小儿画的对不对，如回答“不对”，问哪里画错了',
    '主试者分别问小儿火警、匪警(找警察帮助)、急救电话是多少?',
    '出示猫头鹰抓老鼠图片，主试者问小儿画的对不对，如回答“不对”，问哪里画错了',
]
societyResult = [
    '婴儿能注视主试者的脸',
    '眼睛随走动的人转动',
    '婴儿能自发出现微笑,但不一定出声。睡眠时微笑不通过',
    '经逗引，婴儿会出现微笑、发声、手脚乱动等一种或多种表现',
    '婴儿见到人自行笑起来',
    '婴儿不经逗引可观察周围环境，眼会东张西望',
    '婴儿可经逗引或自发注视镜中人像',
    '观察或询问，在见到母亲或其他亲人时，婴儿会变得高兴起来',
    '对镜中自己的影像有面部表情变化或伴有肢体动作。',
    '观察或询问，当婴儿看到奶瓶或母亲乳房时，表现出高兴要吃的样子',
    '能将饼干送入口中并咀嚼,有张嘴咬的动作而不是吸吮',
    '第三次呼唤婴儿时，婴儿视线再次转向主试者刚才露脸的方向',
    '婴儿能抱住脚玩或吸吮',
    '婴儿有拒抱、哭、不高兴或惊奇等表现',
    '婴儿表现出委屈或兴奋等反应',
    '观察或询问，婴儿对不要之物有摇头或推开的动作',
    '婴儿会用眼睛注视或指出2种或以上的人或物',
    '婴儿能理解指令并成功拿对其中一种或一-种以上物品',
    '观察或询问，婴儿能从杯中喝到水',
    '婴儿能用单手或双手摘下帽子',
    '穿衣时小儿合作，会有伸手、伸腿等配合动作，不一定穿进去',
    '小儿有共同注意过程',
    '观察或询问，小儿能正确且有意识地脱下袜子',
    '经人提醒或主动示意大小便，白天基本不尿湿裤子',
    '小儿能自己用匙吃饭，允许少量遗洒',
    '小儿会说出三种或以上的需要，如“吃饭、喝水、玩汽车、上街”等，可伴手势',
    '小儿有想象性游戏',
    '小儿会自发或模仿说“你好”、“再见”等',
    '小儿会自发提出问题，主动问“这是什么?”',
    '小儿不用帮忙，自己脱掉单衣或单裤',
    '小儿摇头或说出不对',
    '小儿会将水来回倒两次，不洒水',
    '小儿能正确回答或指出应该扔垃圾筐',
    '小儿会穿进鞋并将鞋提上，不要求分左右',
    '小儿会自己解开某一个扣子',
    '小儿能正确回答两问或以上吃饭、穿衣、休息等',
    '小儿能自己扣上娃娃的某一个扣子',
    '小儿无需大人帮忙，会穿上衣并将扣子扣好或拉锁拉好',
    '小儿能回答出原因“为避免生病”等',
    '小儿能主动参加集体游戏，并能遵守游戏规则',
    '小儿能正确识别标志并用语言表达出性别意义',
    '两问均回答正确',
    '小儿会心算出两手有十个手指',
    '小儿说出的住址可使他人较容易找到',
    '小儿能正确回答。为了安全，如怕被汽车撞了等',
    '小儿能正确回答鸡不能在水里游泳',
    '春、夏、秋、冬,顺序可以颠倒',
    '两组图均正确指出危险的标志，并说对理由',
    '小儿均能正确说出',
    '小儿能正确回答下雨了，不能在雨里看书，会淋湿、生病、书湿了',
    '小儿能正确回答出两种或以上电话号码',
    '小儿能正确回答猫头鹰白天睡觉,不会在白天出来抓老鼠'
]

suggest = {'bigTest': bigTest, 'bigResult':bigResult,'fineTest':fineTest,
           'fineResult':fineResult, 'adaptTest':adaptTest, 'adaptResult':adaptResult,
           'languageTest':languageTest, 'languageResult':languageResult,
           'societyTest':societyTest, 'societyResult':societyResult}



with open('C:\\Users\\fakeQ\\Desktop\\页面\\行为.html', 'r') as f:
    contents = f.read()


soup = BeautifulSoup(contents, "html.parser")

index = 0
for tag in soup.find_all('div', class_='action-month'):
    classification,month = tag['id'].split('_')
    classification = classification.replace('Month','')
    table_name = 'rd_scale_action_' + classification

    for quest in tag.find_all('div', class_='title-div'):
        type, id_ = quest['id'].split('_')
        name = quest.find('div', class_='title-font').get_text().replace('\n','').replace(" ", "")
        labels = quest.find_all('label')

        tmp_str = '['
        for label in labels:
            input_ = label.find('input')
            tmp_str = tmp_str + '{"lable":"' + label.get_text().replace('\n','') + '",'
            tmp_str = tmp_str + '"value":' + input_['value'] + ',' + '"type":2},'

            topicField = input_['name']

        tmp_str = tmp_str + ']'

        sug_str = '[{"method":"'+ suggest[type+'Test'][int(id_)-1] +'","pass":"'+  suggest[type+'Result'][int(id_)-1] +'"}]'
        print(index,'|',name,'|',2,'|',table_name,'|',tmp_str,'|',
              topicField,'|', index,'|', sug_str)
        index += 1

    break





####################################互动

with open('C:\\Users\\fakeQ\\Desktop\\页面\\互动.html', 'r') as f:
    contents = f.read()


soup = BeautifulSoup(contents, "html.parser")

index = 0
for tag in soup.find_all('div', class_='title-div'):
    # print(tag)

    titile = tag.find('div', class_='title-font').get_text()
    # print(titile)
    labels = tag.find_all('label')

    tmp_str = '['
    for label in labels:
        input_ = label.find('input')
        tmp_str = tmp_str + '{"lable":"' + label.get_text().replace('\n', '') + '",'
        tmp_str = tmp_str + '"value":' + input_['value'] + ',' + '"type":2},'

        topicField = input_['name']
    tmp_str = tmp_str + ']'

    # print(tmp_str)
    # print('\n')


    print(index, '|', titile, '|', 2, '|', 'rd_scale_interactive', '|', tmp_str, '|',
          topicField, '|', index, '|', "")
    index += 1

    break




