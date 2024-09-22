from yaml import safe_load

def load_config(config_file_path: str):
    """Loads the configuration from the YAML file."""
    with open(config_file_path, 'r') as file:
        config = safe_load(file)
    return config


def merge_args_with_config(args, config) -> dict:
    """Merge command line arguments with config values, giving priority to args."""
    def get_value(arg_value, config_value, default_value):
        return arg_value if arg_value is not None else config_value if config_value is not None else default_value

    return {
        'view_number': get_value(args.view_number, config.get('view_number'), 50),
        'batch_size': get_value(args.batch_size, config.get('batch_size'), 5),
        'proxy_type': get_value(args.proxy_type, config.get('proxy_type'), 'http'),
        'proxy_test_type': get_value(args.proxy_test_type, config.get('proxy_test_type'), ''),
        'proxy_file': get_value(args.proxy_file, config.get('proxy_file'), ''),
        'premium_proxy': args.premium_proxy if args.premium_proxy else config.get('premium_proxy', False),
        'username': get_value(args.username, config.get('username'), None),
        'password': get_value(args.password, config.get('password'), None),
        'view_chunk': get_value(args.view_chunk, config.get('view_chunk'), 0),
        'health_ratio': get_value(args.health_ratio, config.get('health_ratio'), 0),
        'smtp_server': get_value(args.smtp_server, config.get('smtp_server'), 'smtp.example.com'),
        'smtp_port': get_value(args.smtp_port, config.get('smtp_port'), 587),
        'sender_email': get_value(args.sender_email, config.get('sender_email'), None),
        'receiver_email': get_value(args.receiver_email, config.get('receiver_email'), None),
        'email_username': get_value(args.email_username, config.get('email_username'), None),
        'email_password': get_value(args.email_password, config.get('email_password'), None),

    }
