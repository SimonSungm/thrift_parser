namespace py example

include "common.thrift"

// typedef
typedef i32 UserId
typedef map<string, list<i32>> ScoreMap

enum Status {
    ACTIVE = 1,
    INACTIVE = 2,
    DELETED = 3
}

// Constant
const i32 TestIntConstant = 1234;
const string DefaultName = "unknown";
const list<i32> DefaultScores = [100, 90, 80];
const map<string, i32> DefaultAttributes = {"age": 30, "level": 5};

// Struct
struct TestStruct {
    1: bool sBool
    2: required bool sBoolReq
    3: optional bool sBoolOpt
    4: list<string> sListString
    5: set<i16> sSetI16
    6: map<i32,string> sMapI32String
}

struct User {
    1: UserId id = 0,
    2: string name = "unknown", #这是一条注释
    3: Status status = Status.ACTIVE; # 这是一条注释
    //注释
    4: list<i32> scores = [100, 95, 85],
    5: set<string> tags,
    6: map<string, i32> attributes = DefaultAttributes
    7: byte b;
    8: i8 v8
    9: ScoreMap scores
}
