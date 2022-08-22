def upload_broadcast(instance, filename):
    return 'media/file/%s/%s' % (
        instance.broadcast.title,
        filename,
    )
