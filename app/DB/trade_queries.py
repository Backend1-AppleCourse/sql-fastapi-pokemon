def create_trade_query():
    return """
    INSERT INTO Trades (InitiatorTrainerID, ReceiverTrainerID, InitiatorPokemonID, ReceiverPokemonID, Status, CreatedAt, UpdatedAt)
    VALUES (%s, %s, %s, %s, 'pending', NOW(), NOW())
    """

def update_trade_status_query():
    return """
    UPDATE Trades SET Status = %s, UpdatedAt = NOW() WHERE ID = %s
    """

def get_trade_by_id_query():
    return """
    SELECT * FROM Trades WHERE ID = %s
    """

def get_trade_history_query():
    return """
    SELECT * FROM Trades WHERE InitiatorTrainerID = %s OR ReceiverTrainerID = %s ORDER BY ID DESC
    """
