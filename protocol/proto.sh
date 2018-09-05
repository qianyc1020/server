#!/usr/bin/env bash
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/base.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/game_base.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/gateway.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./service/match.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./service/mission.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./service/signin.proto &