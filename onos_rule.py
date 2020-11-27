import json, os

def create_rule(src, dst):
    print("Create rule of {} and {}".format(src, dst))
    deviceId = "0000000000000001"
    rule_forward = {
                        "priority": 60000,
                        "timeout": 0,
                        "isPermanent": True,
                        "deviceId": "of:" + deviceId,
                        "treatment": {
                            "instructions": [
                                {
                                    "type": "OUTPUT",
                                    "port": "10"
                                }
                            ]
                        },
                        "selector": {
                            "criteria": [
                                {
                                "type": "IPV4_SRC",
                                "ip": src + "/32"
                                },
                                {
                                "type": "IPV4_DST",
                                "ip": dst + "/32"
                                },
                                {
                                    "type": "ETH_TYPE",
                                    "ethType": "0x0800"
                                }
                            ]
                        }
                    }
    rule_backward = {
                        "priority": 60000,
                        "timeout": 0,
                        "isPermanent": True,
                        "deviceId": "of:" + deviceId,
                        "treatment": {
                            "instructions": [
                                {
                                    "type": "OUTPUT",
                                    "port": "10"
                                }
                            ]
                        },
                        "selector": {
                            "criteria": [
                                {
                                "type": "IPV4_SRC",
                                "ip": dst + "/32"
                                },
                                {
                                "type": "IPV4_DST",
                                "ip": src + "/32"
                                },
                                {
                                    "type": "ETH_TYPE",
                                    "ethType": "0x0800"
                                }
                            ]
                        }
                    }

    print(json.dumps(rule_forward, indent=4))
    print(json.dumps(rule_backward, indent=4))
    file = open("rule.json", "w")
    file.write(json.dumps(rule_forward, indent=4))
    file.close()
    os.system("curl -X POST -H 'content-type:application/json' http://localhost:8181/onos/v1/flows/of:" + deviceId + " -d @./rule.json --user onos:rocks")
    file = open("rule.json", "w")
    file.write(json.dumps(rule_backward, indent=4))
    file.close()
    os.system("curl -X POST -H 'content-type:application/json' http://localhost:8181/onos/v1/flows/of:" + deviceId + " -d @./rule.json --user onos:rocks")

    os.system("rm rule.json")

if __name__ == "__main__":
    create_rule("192.168.100.1", "198.70.11.172")
