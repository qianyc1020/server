# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from protocol.game import zhipai_pb2 as game_dot_zhipai__pb2


class ZhipaiStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.settle = channel.unary_unary(
            '/Zhipai/settle',
            request_serializer=game_dot_zhipai__pb2.SettleData.SerializeToString,
            response_deserializer=game_dot_zhipai__pb2.SettleResult.FromString,
        )
        self.shuffle = channel.unary_unary(
            '/Zhipai/shuffle',
            request_serializer=game_dot_zhipai__pb2.ShuffleData.SerializeToString,
            response_deserializer=game_dot_zhipai__pb2.ShuffleResult.FromString,
        )
        self.cheat = channel.unary_unary(
            '/Zhipai/cheat',
            request_serializer=game_dot_zhipai__pb2.ShuffleData.SerializeToString,
            response_deserializer=game_dot_zhipai__pb2.ShuffleResult.FromString,
        )


class ZhipaiServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def settle(self, request, context):
        """结算
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def shuffle(self, request, context):
        """洗牌函数
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cheat(self, request, context):
        """洗牌函数
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ZhipaiServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'settle': grpc.unary_unary_rpc_method_handler(
            servicer.settle,
            request_deserializer=game_dot_zhipai__pb2.SettleData.FromString,
            response_serializer=game_dot_zhipai__pb2.SettleResult.SerializeToString,
        ),
        'shuffle': grpc.unary_unary_rpc_method_handler(
            servicer.shuffle,
            request_deserializer=game_dot_zhipai__pb2.ShuffleData.FromString,
            response_serializer=game_dot_zhipai__pb2.ShuffleResult.SerializeToString,
        ),
        'cheat': grpc.unary_unary_rpc_method_handler(
            servicer.cheat,
            request_deserializer=game_dot_zhipai__pb2.ShuffleData.FromString,
            response_serializer=game_dot_zhipai__pb2.ShuffleResult.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'Zhipai', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
