python -m grpc_tools.protoc -I./ --python_out=./ ./base/base.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./base/game_base.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./base/server_to_game.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./service/match.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./service/mission.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./service/signin.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./game/bairen.proto
python -m grpc_tools.protoc -I./ --python_out=./ ./game/hongbao.proto
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ ./game/zhipai.proto
pause