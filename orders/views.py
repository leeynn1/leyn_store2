import stripe

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy, reverse
from django.conf import settings

from common.views import TitleMixin
from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NI7IcFywMDiRt89tVCqnqan',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    #     baskets = Basket.objects.filter(user=self.request.user)
    #     checkout_session = stripe.checkout.Session.create(
    #         line_items=baskets.stripe_products(),
    #         metadata={'order_id': self.object.id},
    #         mode='payment',
    #         success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
    #         cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
    #     )
    #     return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
    #
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


