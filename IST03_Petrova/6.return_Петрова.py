#1
def calc_age(current_year, birth_year):
    age = current_year - birth_year
    return age

my_age = calc_age(2049, 1993)
dads_age = calc_age(2049, 1953)

print(f"Мне {my_age} лет, а моему отцу {dads_age} лет")

#2
def get_boundaries(target, margin):
    low_limit = target - margin
    high_limit = target + margin
    return low_limit, high_limit

low_limit, high_limit = get_boundaries(100, 20)

print(f"Нижний предел: {low_limit}, верхний предел: {high_limit}")

#3
def repeat_stuff(stuff, num_repeats=10):
    return stuff * num_repeats

lyrics = repeat_stuff("Row", 3) + " Your Boat."
song = repeat_stuff("Ла")

print(lyrics)
print(song)