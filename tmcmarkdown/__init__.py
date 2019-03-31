if __name__ == '__main__':
    import markdown
    from extensions import gifv, imgsrcset
    print(markdown.markdown('foo bar',
                            extensions=[
                                gifv.GifV(),
                                imgsrcset.ImgSrcSet()
                            ]))
