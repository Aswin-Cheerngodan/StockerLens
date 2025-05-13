from src.stock_price.components.price_predict import PricePredictor



class predictionPipeline:
    """Pipeline for prediction"""
    def __init__(self, symbol: str):
        self.symbol = symbol.lower()

    def predict(self):
        predictor = PricePredictor(ticker=self.symbol)
        price = predictor.predict_price()

        return price