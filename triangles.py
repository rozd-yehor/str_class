custom_error = 'Вводить можно только целые числа и числа с плавающей точкой больше нуля.'
final_message = "meknulo"


while True:
    try:
        a = float(input("Введите первую сторону: "))
        if a <= 0:
            print(custom_error)
            continue
    except ValueError:
        print(custom_error)
        continue
    break

while True:
    try:
        b = float(input("Введите вторую сторону: "))
        if b <= 0:
            print(custom_error)
            continue
    except ValueError:
        print(custom_error)
        continue
    break

while True:
    try:
        c = float(input("Введите третью сторону: "))
        if c <= 0:
            print(custom_error)
            continue
    except ValueError:
        print(custom_error)
        continue
    break


if a > b and a > c:
    if b**2 + c**2 == a**2:
        final_message = "Треугольник является прямоугольным."
    else:
        final_message = "У вас непримечательный треугольник."
elif b > a and b > c:
    if a**2 + c**2 == b**2:
        final_message = "Треугольник является прямоугольным."
    else:
        final_message = "У вас непримечательный треугольник."
elif c > a and c > b:
    if a**2 + b**2 == c**2:
        final_message = "Треугольник является прямоугольным."
    else:
        final_message = "У вас непримечательный треугольник."

if a == b == c:
    final_message = "Треугольник является равнобедренным и равносторонним."
elif a == b or a == c:
    if 2*a**2 == b**2 or 2*a**2 == c**2:
        final_message = "Треугольник является равнобедренным и прямоугольным."
    else:
        final_message = "Треугольник является равнобедренным."
elif b == a or b == c:
    if 2*b**2 == a**2 or 2*b**2 == c**2:
        final_message = "Треугольник является равнобедренным и прямоугольным."
    else:
        final_message = "Треугольник является равнобедренным."
elif c == a or c == b:
    if 2*c**2 == a**2 or 2*c**2 == b**2:
        final_message = "Треугольник является равнобедренным и прямоугольным."
    else:
        final_message = "Треугольник является равнобедренным."

if a + b <= c or a + c <= b or b + c <= a:
    final_message = "Такой треугольник не существует."


print(final_message)
