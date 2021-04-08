class TestMarkets:
    def test_markets(self, app_client):
        markets = app_client.markets()
        assert len(markets) > 0
