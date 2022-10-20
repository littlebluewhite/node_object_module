import asyncio


class ValueQueue:
    def __init__(self):
        self.pre = dict()
        self.send = dict()

    def insert_data(self, data: dict):
        for i in data:
            pre_value = self.pre.get(i, None)
            if pre_value:
                if pre_value["value"] != data[i]["value"]:
                    self.send[i] = (data[i])
            else:
                self.send[i] = (data[i])
            self.pre[i] = data[i]

    async def get_data(self):
        while True:
            if self.send:
                return list(self.send.values())
            await asyncio.sleep(2)

    def reset(self):
        self.send = dict()
