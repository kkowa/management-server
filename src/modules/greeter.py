import grpc

from idl.grpc.helloworld import helloworld_pb2, helloworld_pb2_grpc


class Greeter:
    """Wrapper module for external gRPC service."""

    def say_hello(self) -> None:
        """Say hello to gRPC server."""
        with grpc.insecure_channel(
            "localhost:50051"  # TODO: Manage gRPC endpoint as variable (CRAWLER_GRPC_URL)
        ) as channel:
            stub = helloworld_pb2_grpc.GreeterStub(channel)
            response = stub.SayHello(helloworld_pb2.HelloRequest(name="You"))

        print(f"Greeter client received: {response.message}")
