namespace py example

include "common.thrift"

enum Status {
    ACTIVE = 1,
    INACTIVE = 2,
    DELETED = 3
}

struct User {
    1: i32 id,
    2: string name,
    3: optional common.Address address
}
