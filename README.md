# SGF-Editor
Combine the functions of both MultiGo and 101weiqi

基于HapHac的weiqi程序进行了比较大幅度的修改。
原程序是一个围棋游戏，包含19，13，9路棋盘，也包括吃子、打劫等判断，不过没有结果判定。

现程序修改，主要希望实现的功能包括：
1. 实现类似MultiGO有存盘和打开功能的GUI围棋软件
2. 增加类似101模糊搜索棋库的功能。


Version 003 计划
1. 增加读取SGF的功能，目前只要求读取死活题的SGF，不要求读取带有顺序的棋谱或者带有变化答案的死活题。


Version 002 Date 2022/5/26
1. 今天学习了ttkbootstrap，将所有代码改成更好看的ttkbootstrap

Version 001 Date: 2022/5/25
今日实现功能：
1. 增加了右键输入棋盘棋子的功能（当前如果左键是白色棋子，则右键落子时黑色；反之，当前左键是黑色棋子，则右键落子是白色。）
2. 增加了保存棋谱的功能（目前并没有计划实现先后顺序记录棋子的功能）；
3. 增加了取消棋子的功能，如果当前是落黑子，点在已经有黑子的位置上，则当前位置的黑棋直接取消；
4. 增加了覆盖棋子颜色的功能，如果当前是落黑子，点在白子上，则当前位置的白棋直接变成黑棋；
5. 由于增加了变化颜色和右键功能，原程序的吃子判定就不再使用，所以进行了更新。
