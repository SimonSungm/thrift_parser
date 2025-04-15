namespace py example

include "common.thrift"

enum Status {
    ACTIVE = 1,
    INACTIVE = 2,
    DELETED = 3
}

struct User {
    1: i32 id = 0,
    2: string name = "unknown", #这是一条注释
    3: Status status = Status.ACTIVE; # 这是一条注释
    //注释
    4: list<i32> scores = [100, 95, 85],
    5: set<string> tags,
    6: map<string, i32> attributes = {"age": 30, "level": 5}
    7: byte b;
    8: i8 v8
}
