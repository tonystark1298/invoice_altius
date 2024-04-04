from flask import Flask
from flask_restful import Resource, Api, reqparse, abort


app = Flask(__name__)
api = Api(app)

store_invoice_header={"uuid1":{
    "Date": "10-02-2024",
    "InvoiceNumber": 1,
    "CustomerName": "custname1",
    "BillingAddress": "billaddrs1",
    "ShippingAddress": "shipadress1",
    "GSTIN": "gstno1",
    "TotalAmount": 10}
}

store_invoice_items={
    "id":{
        "itemName": "item1",
        "Quantity": 1,
        "Price": 10,
        "Amount": 10
        }
}
store_invoice_billsundry={
    "id":{
        "billSundryName": "billSundryName1",
        "Amount":10
            }    
}


parser_invoice_header = reqparse.RequestParser()
parser_invoice_header.add_argument('id',required=True, type=str, help='id is required')
parser_invoice_header.add_argument('Date', type=str, help='date is required')
parser_invoice_header.add_argument('InvoiceNumber', type=int)
parser_invoice_header.add_argument('CustomerName', type=str)
parser_invoice_header.add_argument('BillingAddress', type=str)
parser_invoice_header.add_argument('ShippingAddress', type=str)
parser_invoice_header.add_argument('GSTIN', type=str,)
parser_invoice_header.add_argument('TotalAmount', type=int,)
args_invoice_header = parser_invoice_header.parse_args()

parser_invoice_item = reqparse.RequestParser()
parser_invoice_item.add_argument('id',required=True, type=str, help='id is required')
parser_invoice_item.add_argument("itemName",type=str)
parser_invoice_item.add_argument("Quantity",type=str)
parser_invoice_item.add_argument("Price",type=str)

parser_invoice_bill_sundry=reqparse.RequestParser()
parser_invoice_bill_sundry.add_argument('id',required=True, type=str, help='id is required')
parser_invoice_bill_sundry.add_argument("billSundryName",type=str)
parser_invoice_bill_sundry.add_argument("Amount",type=str)


class InvoiceHeader():
    def get(self,id):
        if id in store_invoice_header.keys():
            return store_invoice_header[id]
        return f"id is not present"        
    
    def put(self):
        args = parser_invoice_header.parse_args()
        if args['id'] in store_invoice_header.keys():
            return f"{args['id']} is already present"
        invoice_header = {
            "Date": args["Date"],
            "InvoiceNumber": args["InvoiceNumber"],
            "CustomerName": args["CustomerName"],
            "BillingAddress": args["BillingAddress"],
            "ShippingAddress": args["ShippingAddress"],
            "GSTIN": args["GSTIN"],
            "TotalAmount": args["TotalAmount"]}
        store_invoice_header[args['id']]=invoice_header
        
        return store_invoice_header[args['id']] , 201

    def delete(self,id):
        if id in store_invoice_header:
            return store_invoice_header[id]
        return f"id is not present"

class InvoiceItem(Resource):
    def get(self,id):
        if id in store_invoice_items.keys():
            return store_invoice_header[id]
        return "id is not present" 
    
    def put(self):
        args = parser_invoice_item.parse_args()
        if args['id'] in store_invoice_items.keys():
            abort(409, f"{args['id']} is already present")
        invoice_item={
            "itemName": args['itemName'],
            "Quantity": args['Quantity'],
            "Price": args['Price'],
            "Amount": args['Amount']
        }
        if args['Quantity']*[args["Price"]]!=args['Amount']:
            abort(409, f"quantity*price does not match Amount")
        store_invoice_items[args['id']]=invoice_item
        return store_invoice_items[args['id']], 201
    
    def delete(self,id):
        if id in store_invoice_items.keys():
            del store_invoice_header[id]
        return "id was not present"


class InvoiceBillSundry(Resource):
    def get(self,id):
        if id in store_invoice_billsundry.keys():
            return store_invoice_billsundry[id]
        return "id is not present" 
    
    def put(self):
        args = parser_invoice_bill_sundry.parse_args()
        if args['id'] in store_invoice_billsundry.keys():
            return f"{args['id']} is already present"
        invoice_bill_sundry_item={
            "billSundryName": args["billSundryName"],
            "Amount": args['Amount']
        }
        if args["Amount"]>0 or args["Amount"]<=0 :
            abort(409, f"Amount is not correct")
        store_invoice_billsundry[args['id']]=invoice_bill_sundry_item
        return store_invoice_billsundry[args['id']], 201
    
    def delete(self,id):
        if id in store_invoice_items.keys():
            del store_invoice_header[id]
        return "id was not present"
    
    def update(self,id):
        if id in store_invoice_items.keys():
            del store_invoice_header[id]
        return "id was not present"


app.add_resource(InvoiceHeader,'/header')
app.add_resource(InvoiceBillSundry,'/BillSundry')
app.add_resource(InvoiceItem,'/invoiceItem')
app.add_resource(InvoiceHeader.get,'/header/get/<str:id>')
app.add_resource(InvoiceHeader.delete,'/header/delete/<str:id>')
app.add_resource(InvoiceBillSundry.get,'/BillSundry/get/<str:id>')
app.add_resource(InvoiceBillSundry.delete,'/BillSundry/delete/<str:id>')
app.add_resource(InvoiceItem.get,'/invoiceItem/get/<str:id>')
app.add_resource(InvoiceItem.delete,'/invoiceItem/delete/<str:id>')
if __name__==("__main__"):
    app.run(debug="True",port =5001)
    

'''I have taken UUID as str for simplicity'''
''' for the fifth requirements all the data should be taken simultaneously,
 but i assumed that it will be given separately therefore it was difficult to implement'''











