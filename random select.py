import random
# 输入格式：学号,权重
# 读取学号和相应的权重值，并将它们存储在一个字典中
student_weights = {}

with open('input.txt', 'r', ) as f:
    for line in f:
        student_id, weight = line.strip().split(',')
        student_weights[student_id] = float(weight)

# 使用权重进行加权抽取
total_weight = sum(student_weights.values())
selected_students = []
#while len(selected_students) < 100:
if len(selected_students) < 1:
    # 生成一个随机值，用于抽取学号
    r = random.uniform(0, total_weight)
    # 遍历学号及其权重，计算随机值所处的区间
    for student_id, weight in student_weights.items():
        r -= weight
        if r <= 0:
            # 如果随机值处于该学号的区间内，则将该学号添加到选中的学号列表中
            selected_students.append(student_id)
            break

# 输出被选中的学号

print("被选中的学号为：", selected_students[0])
