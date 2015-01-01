"""

Python library for Mageworld's Affiliate Pro Magento Plugin

	http://www.mage-world.com/magento-affiliate-extension.html

Author: Benton Snyder
Website: http://bensnyde.me
Created: 10/28/2014
Revised: 12/31/2014

"""
import MySQLdb as mdb
import logging
import random


logger = logging.getLogger(__name__)

class MW_Affiliates:
    def __init__(self, dbhost, dbuser, dbpass, dbname):
        """ Constructor """
        try:
            self.con = mdb.connect(dbhost, dbuser, dbpass, dbname);
        except Exception as ex:
            logger.error("Failed to initialize: %s" % ex)
            return False


    def __del__(self):
        """ Desctructor """
        try:
            self.con.close()
        except:
            pass


    def get_affiliates(self):
        """ Retrieves Affiliates List """
        try:
            cur = self.con.cursor()
            cur.execute("select customer_id,active,referral_code,payment_gateway,payment_email,auto_withdrawn,withdrawn_level,reserve_level,tax_id,email,referral_code from mg_mw_affiliate_customers join mg_customer_entity on customer_id=entity_id")

            # Append column names to values
            columns = tuple( [d[0].decode('utf8') for d in cur.description] )
            rows = []
            for row in cur.fetchall():
                rows.append(dict(zip(columns, row)))

            return rows

        except mdb.Error, e:
            logger.error("get_affiliates() error %d: %s" % (e.args[0],e.args[1]))
            return False


    def approve_affiliate(self, affiliate_id):
        """ Approves Affiliate """
        try:
            cur = con.cursor()
            cur.execute('update mg_mw_affiliate_customers set active=2, referral_code="%s" where customer_id=%s' % (self.generate_affiliate_code(), affiliate_id))
            self.con.commit()

            if cur.rowcount > 0:
                return True

        except mdb.Error, e:
            logger.error("approve_affiliate(%s) error %d: %s" % (affiliate_id, e.args[0],e.args[1]))

        return False


    def set_taxid(self, affiliate_id, tax_id):  # This is an added field that is not present in the standard MW Affiliates plugin
        """ Updates Affiliate's TaxID """
        try:
            cur = con.cursor()
            cur.execute('update mg_mw_affiliate_customers set tax_id=%s where customer_id=%s' % (tax_id, affiliate_id))
            self.con.commit()

            if cur.rowcount > 0:
                return True

        except mdb.Error, e:
            logger.error("set_taxid(%s, %s) error %d: %s" % (affiliate_id, tax_id, e.args[0],e.args[1]))

        return False


    def generate_affiliate_code(self, code_length=7):
        """ Generate Unique Referral Code """
        valid_opts = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

        while 1:
            response = ""
            for x in xrange(code_length):
                while 1:
                    to_add = random.choice(valid_opts)
                    # Don't allow same value twice
                    if not response.endswith(to_add):
                        response += to_add
                        break

            try:
                cur = self.con.cursor()
                cur.execute('select count(*) from mg_mw_affiliate_customers where referral_code="%s"' % response)

                if not cur.fetchone()[0]:
                    break

            except mdb.Error, e:
                logger.error("generate_affiliate_code(%s) error %d: %s" % (code_length, e.args[0],e.args[1]))
                return False

        return response
