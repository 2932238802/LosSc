#!/usr/bin/bash
find . -type d -name __pycache__ -exec rm -rf {} +
rm -rf data/los_news.db
echo "清理完成"
