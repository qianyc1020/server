#!/usr/bin/env bash
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/base.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/game_base.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/server_to_game.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./base/gateway.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./service/match.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./service/mission.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./service/signin.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./game/bairen.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./game/hongbao.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./game/wuziqi.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./game/jinhua.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ ./game/douniu.proto &
/usr/bin/python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ ./game/zhipai.proto &