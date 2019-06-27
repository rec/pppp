if __name__ == '__main__':
    pppp = open('pppp.py').read()
    tmpl = open('pppp.sh.tmpl').read()
    with open('pppp.sh', 'w') as fp:
       fp.write(tmpl.format(pppp))
       print('Wrote pppp.sh')
