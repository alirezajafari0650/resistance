def upload_broadcast(instance, filename):
    filename = filename.replace(' ', '_')
    filename = filename.replace('\u200c', '_')
    foldername = instance.broadcast.title
    foldername = foldername.replace(' ', '_')
    foldername = foldername.replace('\u200c', '_')
    return 'file/%s/%s' % (
        foldername,
        filename,
    )
