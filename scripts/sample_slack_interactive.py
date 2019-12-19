
def is_valid_access(workspace_name, request):
    if len(Workspace.objects.filter(workspace_name=workspace_name)) > 0:

        if 'X-Slack-Signature' in request.headers:
            timestamp = request.headers['X-Slack-Request-Timestamp']

            # 5分より前のリクエストの場合、拒否
            if (int(datetime.now().strftime("%s")) - int(timestamp)) > 60*5:
                return False

            sigining_secret_val = request.headers['X-Slack-Signature']

            workspace_obj = Workspace.objects.filter(
                workspace_name=workspace_name)[0]

            workspace_signing_secret = workspace_obj.bot_signing_secret

            sig_basestring = 'v0:' + timestamp + ':' + request.body.decode()

            # HMAC-SHA256 keyed hashを計算
            hash_val = hmac.new(
                workspace_signing_secret.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()

            # logger.debug(hash_val)
            # logger.debug(sigining_secret_val)

            if sigining_secret_val == 'v0=' + hash_val:
                return True

    return False


def interactive_component(request, workspacename):
    logger.debug('interactive component')

    if not is_valid_access(workspacename, request):
        raise PermissionDenied('Not authorized')

    if request.method == 'POST':
        # logger.debug(request.POST)
        if is_JSON_Format(request.POST['payload'].replace('\\', '')):
            logger.debug('json')
            json_data = json.loads(request.POST['payload'].replace('\\', ''))

            result = parse_interactive_component(json_data)
            logger.debug(json.dumps(json_data))
            # logger.debug(request.body)

    return HttpResponse(result)


def parse_interactive_component(json_parm):
    '''
    Interactive component をパースする
    '''

    if json_parm['type'] != "interactive_message":
        return 'not found'

    ans = json_parm['actions'][0]['value']
    user = json_parm['user']['id']
    channel = json_parm['channel']['id']
    response_url = json_parm['response_url']

    workspacename = json_parm['team']['domain']
    callback_id = json_parm['callback_id']

    # Callback_id で判定
    if callback_id == 'workbook_select':
        result = select_workbook_callback(workspacename, user, ans)
        if result != 'NG':
            return result
    elif callback_id == 'workbook_question':
        result = check_answer(workspacename, channel, user, ans)
        if result != 'NG':
            return result
    elif callback_id == 'resume_hook':
        result = check_resume_answer(workspacename, channel, user, ans)
        return result

    reply_msg = 'You select ' + ans
    return reply_msg
