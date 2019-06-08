

def wr(x, wrap, end_wrap=None):
    return (
        f'{wrap}{x}{wrap}'
        if not end_wrap
        else f'{wrap}{x}{end_wrap}'
    )
