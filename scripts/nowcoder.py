import pandas as pd
import pygal


class INFO:
    '''
    每个队伍每次比赛的成绩信息
    rk: 排名
    ac: 过题数
    penalty: 罚时
    '''
    rk = 0
    ac = 0
    penalty = ''

    def __init__(self, rk, ac, penalty):
        self.rk = rk
        self.ac = ac
        self.penalty = penalty


class TEAM:
    '''
    每个队伍的类
    name: 队伍名称
    p1: 同学1
    p2: 同学2
    p3: 同学3
    num: 队伍表示编码
    avg: 平均分
    infos: 存储每次比赛的成绩信息
    '''
    name = ''
    p1 = ''
    p2 = ''
    p3 = ''
    num = 0
    avg = 0
    infos = []

    def __init__(self, name, p1, p2, p3, num):
        self.name = str(name)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.num = num
        self.avg = 0
        self.infos = []


NUM = 8


def assio(teams, name_num):
    df = pd.read_excel('../sheets/team.xlsx')  # 获取队名与队员映射
    for i in range(NUM):
        teams.append(TEAM(df.iloc[i][1], df.iloc[i][2], df.iloc[i][3], df.iloc[i][4], i))
        name_num[str(teams[i].name)] = i
    return


def read(teams, name_num):
    # Read the data from the excel file
    file = pd.read_excel('../sheets/nowcoder.xlsx', sheet_name=None)
    # get sheet num
    sheet_num = len(file)
    # 输出第一行
    for i in range(1, sheet_num + 1):
        df = file.get(str(i))  # 获取当前场的队伍信息
        # print(df)
        for i in range(NUM):  # 队伍当前场次信息存入
            if (df.iloc[i][0] == '#'):
                teams[name_num[str(df.iloc[i][1])]].infos.append(INFO(None, 0, 0))
            else:
                teams[name_num[str(df.iloc[i][1])]].infos.append(INFO(int(df.iloc[i][0]), int(df.iloc[i][2]), df.iloc[i][3]))
            # print(df.iloc[i][1],df.iloc[i][0], df.iloc[i][2], df.iloc[i][3])
    # for team in teams:
    #     print(team.num,team.name)
    #     for info in team.infos:
    #         print(info.rk, info.ac, info.penalty,end='|')
    #     print()
    return


def update(teams):
    for team in teams:
        team.avg = 0
        cnt = 0
        for info in team.infos:
            if (info.rk == None):
                cnt += 1
            else:
                team.avg += info.rk
        team.avg /= (len(team.infos) - cnt)
    return


def draw(teams):
    # 排名统计图
    line_chart = pygal.Line(
        title='牛客多校训练排名统计',
        legend_at_bottom=True,
        legend_at_bottom_columns=3,
        inverse_y_axis=True,
        interpolate='cubic',
        width=1200,
        height=550,
    )
    line_chart.config.style.title_font_size = 14
    line_chart.config.style.label_font_size = 14
    line_chart.config.style.major_label_font_size = 14
    line_chart.x_labels = iter(['第' + str(x) + '场' for x in range(1, len(teams[0].infos) + 1)] + ['平均排名'] + ['第' + str(x) + '场' for x in range(len(teams[0].infos) + 1, 11)])
    line_chart.y_labels = 50, 150, 300
    for team in teams:
        line_chart.add(team.name + '({}+{}+{})'.format(team.p1, team.p2, team.p3), [info.rk for info in team.infos] + [team.avg])
        # print(type(team.name),type(team.p1),type(team.p2),type(team.p3))
    line_chart.render_to_file('./nowcoder/nowcoder_line.svg')

    bar_chart = pygal.HorizontalBar(
        title='牛客多校训练表现统计',
        legend_at_bottom_columns=5,
        legend_at_bottom=True,
        width=1200,
        height=550,
    )
    bar_chart.x_labels = iter([team.name + '({})'.format(team.p1) for team in teams])
    bar_chart.y_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    base_cnt = []
    gold_cnt = []
    silver_cnt = []
    bronze_cnt = []
    for team in teams:
        base_cnt.append(sum([info.rk != None and info.rk <= 500 for info in team.infos]))
        bronze_cnt.append(sum([info.rk != None and info.rk > 150 and info.rk <= 300 for info in team.infos]))
        silver_cnt.append(sum([info.rk != None and info.rk > 50 and info.rk <= 150 for info in team.infos]))
        gold_cnt.append(sum([info.rk != None and info.rk > 0 and info.rk <= 50 for info in team.infos]))
    bar_chart.add('金牌', gold_cnt)
    bar_chart.add('银牌', silver_cnt)
    bar_chart.add('铜牌', bronze_cnt)
    bar_chart.add('签到', base_cnt)
    bar_chart.render_to_file('./nowcoder/nowcoder_bar.svg')

    pie_chart = pygal.Pie(
        title='牛客多校训练过题统计',
        legend_at_bottom=True,
        legend_at_bottom_columns=3,
        width=1200,
        height=550,
    )
    for team in teams:
        pie_chart.add(team.name + '({}+{}+{})'.format(team.p1, team.p2, team.p3), sum([info.ac for info in team.infos]))
    pie_chart.render_to_file('./nowcoder/nowcoder_pie.svg')
    return


if __name__ == '__main__':
    teams = []
    name_num = {}
    num_name = {}
    assio(teams, name_num)
    read(teams, name_num)
    update(teams)
    draw(teams)