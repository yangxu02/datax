# -*- coding: utf-8 -*-

import datetime
import time
import sys

import ConfigParser
from SQLBasedSupplier import SQLBasedSupplier
from HiveBasedSupplier import HiveBasedSupplier
from HttpBasedSupplier import HttpBasedSupplier
from MultiSQLBasedSupplier import MultiSQLBasedSupplier
from EmailBasedSinker import EmailBasedSinker
from MultiSectionEmailSinker import MultiSectionEmailSinker
from HttpBasedSinker import HttpBasedSinker
from MultiSectionHttpSinker import MultiSectionHttpSinker
from MultiSectionCsvSinker import MultiSectionCsvSinker
from GroupEmailSinker import GroupEmailSinker
from BaseSupplier import BaseSupplier
from BaseSinker import BaseSinker
from BaseExtender import BaseExtender
from KeyBasedExtender import KeyBasedExtender
from MultiStageKeyExtender import MultiStageKeyExtender
from lib import Logger

class Worker:

    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.conf_file)

    
    def run(self, task):
        Logger.d("[Executor-%s]" % task, "start running at " + str(datetime.datetime.now()))

        if not self.config.has_section(task):
            Logger.f("[Executor-%s]" % task, "failed running at {0}, reason={1}".format(datetime.datetime.now(), "task not found"))
            return

        supplier = None
        supplier_type = self.config.get(task, "supplier.type").lower()
        Logger.d("[Executor-%s]" % task, "supplier_type=%s" % (supplier_type))
        if "sql" == supplier_type or "mysql" == supplier_type:
            supplier_db_name = self.config.get(task, "supplier.db_name")
            supplier_sql_file = self.config.get(task, "supplier.sql_file")
            supplier_cachable = False
            if self.config.has_option(task, "supplier.cachable"):
                supplier_cachable = self.config.get(task, "supplier.cachable")
            supplier_sql = ""
            with open(supplier_sql_file, "r") as sql_file:
                supplier_sql = sql_file.read()

            #Logger.d("[Executor-%s]" % task, "db=%s file=%s sql=%s" % (supplier_db_name, supplier_sql_file, supplier_sql))
            supplier = SQLBasedSupplier(task, supplier_db_name, supplier_sql, supplier_cachable)

        elif "hql" == supplier_type or "hive" == supplier_type:
            supplier_db_name = self.config.get(task, "supplier.db_name")
            supplier_sql_file = self.config.get(task, "supplier.sql_file")
            supplier_tmp_file = None
            if self.config.has_option(task, "supplier.tmp_file"):
                supplier_tmp_file = self.config.get(task, "supplier.tmp_file")
            supplier_cachable = False
            if self.config.has_option(task, "supplier.cachable"):
                supplier_cachable = self.config.get(task, "supplier.cachable")
            supplier_sql = ""
            with open(supplier_sql_file, "r") as sql_file:
                supplier_sql = sql_file.read()

            #Logger.d("[Executor-%s]" % task, "db=%s file=%s sql=%s" % (supplier_db_name, supplier_sql_file, supplier_sql))
            supplier = HiveBasedSupplier(task, supplier_db_name, supplier_sql, supplier_tmp_file, supplier_cachable)

        elif "multi-sql" == supplier_type:
            supplier_db_name = self.config.get(task, "supplier.db_name")
            supplier_cachable = False
            if self.config.has_option(task, "supplier.cachable"):
                supplier_cachable = self.config.get(task, "supplier.cachable")
            supplier_instances = self.config.get(task, "supplier.instances").split(",")
            supplier_sqls = {}
            for instance in supplier_instances:
                instance_sql_file = self.config.get(task, "supplier." + instance + ".sql_file")
                with open(instance_sql_file, "r") as sql_file:
                    instance_sql = sql_file.read()
                    supplier_sqls[instance] = {"sql":instance_sql}

            supplier = MultiSQLBasedSupplier(task, supplier_db_name, supplier_sqls, supplier_cachable)

        elif "http" == supplier_type:
            supplier_product = self.config.get(task, "supplier.product")
            supplier_cq = self.config.get(task, "supplier.cq")
            supplier_dimen = self.config.get(task, "supplier.dimen")
            supplier_log_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
            if self.config.has_option(task, "supplier.date"):
                supplier_date = self.config.get(task, "supplier.date")
                if '{INTERVAL}' == supplier_date:
                    supplier_date_interval = self.config.get(task, "supplier.date.interval")
                    date_tmp = datetime.date.today() - datetime.timedelta(days=int(supplier_date_interval))
                    supplier_log_date = datetime.datetime.strftime(date_tmp, "%Y-%m-%d")
            supplier_filters = {}
            if self.config.has_option(task, "supplier.filters"):
                supplier_filter_dims = self.config.get(task, "supplier.filters").split(",")
                for dim in supplier_filter_dims:
                    dimValues = self.config.get(task, "supplier.filters." + dim).split(",") 
                    supplier_filters[dim] = dimValues

            supplier = HttpBasedSupplier(task, supplier_log_date, supplier_product, supplier_dimen, supplier_cq, supplier_filters)
        elif "test" == supplier_type:
            supplier = SimpleTestSupplier()

        if supplier is None:
            Logger.e("[Executor-%s]" % task, "no supplier, abort")
            return

        sinker = None
        sinker_type = self.config.get(task, "sinker.type").lower()
        if "html" == sinker_type:
            sinker_title = self.config.get(task, "sinker.title")
            sinker_cols = self.config.get(task, "sinker.cols")
            sinker_html_format = self.config.get(task, "sinker.format")

            sinker = HttpBasedSinker(task, sinker_title, sinker_cols, sinker_html_format)

        elif "multi-html" == sinker_type:
            sinker_title = self.config.get(task, "sinker.title")
            sinker_instances = self.config.get(task, "sinker.instances").split(",")
            sinker_contexts = []
            for instance in sinker_instances:
                instance_title = self.config.get(task, "sinker." + instance + ".title")
                instance_cols = self.config.get(task, "sinker." + instance + ".cols")
                sinker_contexts.append({"id":instance, "title":instance_title, "cols":instance_cols})

            sinker = MultiSectionHttpSinker(task, sinker_title, sinker_contexts)

        elif "email" == sinker_type:
            sinker_title = self.config.get(task, "sinker.title")
            sinker_cols = self.config.get(task, "sinker.cols")
            sinker_address = self.config.get(task, "sinker.address")

            sinker = EmailBasedSinker(task, sinker_address, sinker_title, sinker_cols)

        elif "multi-email" == sinker_type:
            sinker_address = self.config.get(task, "sinker.address")
            sinker_title = self.config.get(task, "sinker.title")
            sinker_instances = self.config.get(task, "sinker.instances").split(",")
            sinker_contexts = []
            for instance in sinker_instances:
                instance_title = self.config.get(task, "sinker." + instance + ".title")
                instance_cols = self.config.get(task, "sinker." + instance + ".cols")
                sinker_contexts.append({"id":instance, "title":instance_title, "cols":instance_cols})

            sinker = MultiSectionEmailSinker(task, sinker_address, sinker_title, sinker_contexts)

        elif "multi-csv" == sinker_type:
            sinker_instances = self.config.get(task, "sinker.instances").split(",")
            sinker_contexts = []
            for instance in sinker_instances:
                instance_write_header = self.config.get(task, "sinker." + instance + ".write_header")
                instance_cols = self.config.get(task, "sinker." + instance + ".cols")
                instance_output = self.config.get(task, "sinker." + instance + ".output")
                sinker_contexts.append({"id":instance, "write_header":instance_write_header, "cols":instance_cols, "output":instance_output})

            sinker = MultiSectionCsvSinker(task, sinker_contexts)

        elif "group-email" == sinker_type:
            sinker_address = self.config.get(task, "sinker.address")
            sinker_title = self.config.get(task, "sinker.title")
            sinker_cols = self.config.get(task, "sinker.cols")
            sinker_group_by = self.config.get(task, "sinker.group_by")
            sinker_limit = sys.maxint
            if self.config.has_option(task, "sinker.limit"):
                sinker_limit = self.config.get(task, "sinker.limit")

            sinker = GroupEmailSinker(task, sinker_address, sinker_title, sinker_cols, sinker_group_by, sinker_limit)


        if sinker is None:
            Logger.e("[Executor-%s]" % task, "no sinker, abort")
            return


        extender = None
        extender_type = ""
        if self.config.has_option(task, "extender.type"):
            extender_type = self.config.get(task, "extender.type").lower()
        if "single-key" == extender_type:
            supplier_type = self.config.get(task, "extender.supplier.type")
            extender_supplier = None
            if "sql" == supplier_type or "mysql" == supplier_type:
                supplier_db_name = self.config.get(task, "extender.supplier.db_name")
                supplier_sql_file = self.config.get(task, "extender.supplier.sql_file")
                supplier_cachable = False
                if self.config.has_option(task, "extender.supplier.cachable"):
                    supplier_cachable = self.config.get(task, "extender.supplier.cachable")
                supplier_sql = ""
                with open(supplier_sql_file, "r") as sql_file:
                    supplier_sql = sql_file.read()

                #Logger.d("[Executor-%s]" % task, "db=%s file=%s sql=%s" % (supplier_db_name, supplier_sql_file, supplier_sql))
                extender_supplier = SQLBasedSupplier(task, supplier_db_name, supplier_sql, supplier_cachable)
            if not extender_supplier is None:
                extender_base_key_index = self.config.get(task, "extender.base_key_index")
                extender_data_key_index = self.config.get(task, "extender.data_key_index")
                extender_insert_index = self.config.get(task, "extender.insert_index")

                extender = KeyBasedExtender(task, extender_supplier, extender_base_key_index, extender_data_key_index, extender_insert_index)

        if "multi-stage" == extender_type:
            extender_stages = self.config.get(task, "extender.stages").split(',')
            contexts = []
            for stage in extender_stages:
                prefix = "extender." + stage + "."
                supplier_type = self.config.get(task, prefix + "supplier.type")
                extender_supplier = None
                if "sql" == supplier_type or "mysql" == supplier_type:
                    supplier_db_name = self.config.get(task, prefix + "supplier.db_name")
                    supplier_sql_file = self.config.get(task, prefix + "supplier.sql_file")
                    supplier_cachable = False
                    if self.config.has_option(task, prefix + "supplier.cachable"):
                        supplier_cachable = self.config.get(task, prefix + "supplier.cachable")
                    supplier_sql = ""
                    with open(supplier_sql_file, "r") as sql_file:
                        supplier_sql = sql_file.read()

                    #Logger.d("[Executor-%s]" % task, "db=%s file=%s sql=%s" % (supplier_db_name, supplier_sql_file, supplier_sql))
                    extender_supplier = SQLBasedSupplier(task, supplier_db_name, supplier_sql, supplier_cachable)
                if not extender_supplier is None:
                    extender_base_key_index = self.config.get(task, prefix + "base_key_index")
                    extender_data_key_index = self.config.get(task, prefix + "data_key_index")
                    extender_insert_index = self.config.get(task, prefix + "insert_index")

                    contexts.append({"supplier":extender_supplier, "base_key_index":extender_base_key_index, "data_key_index":extender_data_key_index, "insert_index":extender_insert_index})

            extender = MultiStageKeyExtender(task, contexts)



        data = supplier.get()
        if not extender is None:
            data = extender.extend(data)

        data =  sinker.sink(data)

        Logger.d("[Executor-%s]" % task, "end running at " + str(datetime.datetime.now()))

        return data
