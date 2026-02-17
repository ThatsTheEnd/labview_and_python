import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        # ask user for two numbers to add
        input1 = float(input("Enter the first number: "))
        input2 = float(input("Enter the second number: "))
        response = stub.Add(calculator_pb2.AddRequest(number1=input1, number2=input2))
        print("Result:", response.result)

if __name__ == '__main__':
    run()
