#view page, must registed in app.__init__.py first
import time
from app import app
from flask_login import login_required
from flask import render_template,request,redirect
from app.mod_commodity.models import Commodity
import app.mod_commodity.controllers as c
from app.mod_commodity.blockchain import Block
from app.mod_publisher.zmqpublisher import publisher,conf
import qrcode
import threading


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_commodities') }}"> 或  href="/commoditylist"都可以路由到这里
@app.route('/commoditylist')
@login_required
def list_all_commodities():
    commodity = c.get_all_data()
    print(commodity)
    return render_template("commodity/commoditylist.html",commoditylist= commodity)


@app.route('/blockchainlist')
@login_required
def list_all_blockchains():
    commodity = c.get_all_blocks()
    return render_template("commodity/blockchainlist.html",commoditylist= commodity)

@app.route('/searchlist')
@login_required
def list_all_search():
    return render_template("commodity/searchlist.html")


@app.route('/savecommodity', methods=['POST'])
@login_required
def save_commodity():

    commodity = Commodity()
    commodity.location = request.form["location"]
    commodity.person = request.form["person"]
    commodity.tel = request.form["tel"]
    commodity.desc = request.form["desc"]
    commodity.event_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    commodity.event_name = request.form["eventname"]

    if(not request.form["recordid"]=='None'):
        commodity.id = int(request.form["recordid"])
    else:
        commodity.id = 0

    c.insert_data(commodity)

    return redirect('/commoditylist')


@app.route('/deletecommodity/<int:id>')
@login_required
def delete_commodity(id):
    commodity = c.select_by_id(id)
    c.delete_by_id(commodity)
    return redirect('/commoditylist')


@app.route('/editcommodity/<int:id>')
@login_required
def edit_commodity(id):
    commodity = Commodity()
    if(id != 0):
        commodity = c.select_by_id(id)
    print(commodity.__dict__)
    return render_template("commodity/commodityform.html",selectcommodity= commodity)


@app.route('/addblock/<int:id>')
@login_required
def add_new_block(id):

    block_data = ''
    #get status='Y'
    block_in_chain = c.get_all_blocks()

    #qr list data
    qr_list = block_in_chain.copy()

    #chain_index +1
    _index = len(block_in_chain) + 1

    #set transaction value
    new_block = c.select_by_id(id)
    transaction = "{},{},{},{},{},{}".format(new_block.event_name, new_block.event_time, new_block.location,
                                                new_block.person, new_block.tel, new_block.desc)
    print(transaction)
    qr_list.append(new_block)



    #first block of the chain
    if(_index==1):

        block = Block(_index,transaction,'0')
        #print(block.proof_of_work(block),'---------',block.nonce)
        cur_hash = block.proof_of_work(block)
        nonce = block.nonce

        commodity = Commodity()
        commodity.id = id
        commodity.current_hash = cur_hash
        commodity.random_num = nonce
        commodity.chain_index = _index
        commodity.pre_hash = '0'
        commodity.status = 'Y'

        c.update_hash_data(commodity)

        #for qrcode
        #block_in_chain.append(commodity)


    else:
        #get last chain's hash
        pre_hash = block_in_chain[-1].current_hash
        block = Block(_index,transaction,pre_hash)

        #pub-sub pattern
        pub = publisher(conf['private_server'],conf['port'],'new_block')
        #pub.publish_newblock(block)
        _pub_thread = threading.Thread(target=pub.publish_newblock,kwargs={'data':block})
        _pub_thread.start()

        #get finished status
        _status = publisher(conf['private_server'],conf['signal_port'],'')
        _status_thread = threading.Thread(target=_status.req_rep)
        _status_thread.start()

        cur_hash = block.proof_of_work(block)
        nonce = block.nonce

        commodity = Commodity()
        commodity.id = id
        commodity.current_hash = cur_hash
        commodity.random_num = nonce
        commodity.chain_index = _index
        commodity.pre_hash = pre_hash
        commodity.status = 'Y'

        c.update_hash_data(commodity)
        # for qrcode
        #block_in_chain.append(commodity)


    i = 0
    qr_data = ''
    for blockdata in qr_list:
        i += 1
        temp_data = "{},{},{},{},{},{}".format(blockdata.event_name, blockdata.event_time, blockdata.location,
                                               blockdata.person, blockdata.tel, blockdata.desc)
        qr_data += 'block{}:{}'.format(i,temp_data)


    img = qrcode.make(qr_data)
    img.save(app.static_folder + '/img/' + 'block'+str(i)+'.png')

    return redirect('/commoditylist')





