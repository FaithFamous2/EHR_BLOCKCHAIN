# blockchain.py

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block in the chain
        genesis_block = Block("Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        # Add a new block to the chain
        previous_block = self.chain[-1]
        new_block = Block(data, self.calculate_hash(previous_block))
        self.chain.append(new_block)

    def calculate_hash(self, block):
        # Calculate the hash of a block (in a real blockchain, this would be a complex cryptographic hash)
        return str(hash(block.data) + hash(block.previous_hash))
    def add_ehr_to_blockchain(self, ehr_data):
        # Add an EHR block to the blockchain
        ehr_block = Block(ehr_data, self.calculate_hash(self.chain[-1]))
        self.chain.append(ehr_block)

    def verify_ehr(self, ehr_id):
        # Verify the integrity of an EHR block
        if ehr_id < len(self.chain):
            ehr_block = self.chain[ehr_id]
            previous_block = self.chain[ehr_id - 1]
            is_valid = self.calculate_hash(previous_block) == ehr_block.previous_hash
            return ehr_block.data, is_valid
        return None, False
    def add_appointment(self, appointment_data):
        # Add an appointment block to the blockchain
        appointment_block = Block(appointment_data, self.calculate_hash(self.chain[-1]))
        self.chain.append(appointment_block)

    def verify_appointment(self, appointment_id):
        # Verify the integrity of an appointment block
        if appointment_id < len(self.chain):
            appointment_block = self.chain[appointment_id]
            previous_block = self.chain[appointment_id - 1]
            is_valid = self.calculate_hash(previous_block) == appointment_block.previous_hash
            return appointment_block.data, is_valid
        return None, False
