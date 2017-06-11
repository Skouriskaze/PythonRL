import random

def main():
    while True:
        line = raw_input('Input (#d#): ')
        try:
            num, faces = [int(x) for x in line.split('d')]
            rolls = [random.randint(1, faces) for i in range(num)]
            print ('%s, %s' % (rolls, sum(rolls)))
            print ''
        except Exception as e:
            print e.message
            print "Invalid input, try again."


if __name__ == '__main__':
    main()
