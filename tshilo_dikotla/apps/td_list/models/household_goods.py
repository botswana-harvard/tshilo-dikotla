from edc_base.model.models import ListModelMixin


class HouseholdGoods (ListModelMixin):

    class Meta:
        app_label = 'td_list'
        verbose_name = "Household Goods"
        verbose_name_plural = "Household Goods"
