#!/bin/sh

gunicorn src.web.app:'app'