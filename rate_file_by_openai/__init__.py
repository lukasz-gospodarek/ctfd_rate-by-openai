from flask import Blueprint

from CTFd.models import Challenges, db
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.migrations import upgrade

from . import process_file


PLUGIN_NAME = "rate_file_by_openai" # The same as the directory name in CTFd/plugins


def load(app):
    upgrade(plugin_name="rate_file_by_openai")
    api_route = next((r.rule for r in app.url_map.iter_rules() if r.endpoint == "api.root"), "/api/v1").rstrip("/")
    # Register the endpoints that we want to use
    app.route(api_route + "/scripts/rate_file_by_openai", methods=["POST"])(process_file.upload_file)