if __name__ == '__main__':
    import markdown
    from .extentions import gifv
    print(markdown.markdown('foo bar', extensions=[gifv.GifV()]))
