class Query(ObjectType):
    rate = List(
        items=List(default_value="ERROR"),
        name=String(default_value="ERROR"),
        code=String(default_value="ERROR"),
        time=String(default_value="ERROR"),
    )
    def resolve_rate(root, info, cose, name, code, time):
        return f'Your cose: {cose}, the service name and code: {name}-{code}, and the transittime: {time}'

