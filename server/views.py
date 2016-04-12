from server.models import UserProfile, Restaurant, MenuItem, Menu, Table, Order
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, ListView, UpdateView
from server.forms import ServerCreateForm, CreateOrderForm, OrderFormSet
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


class LandingView(TemplateView):
    template_name = 'landing.html'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['user'] = self.request.user
        employee_list = UserProfile.objects.filter(workplace=self.request.user.userprofile.workplace)
        context['servers'] = employee_list.filter(position='S')
        context['kitchen'] = employee_list.filter(position='K')
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm

    def form_valid(self, form):
        user_object = form.save()
        new_restaurant = Restaurant.objects.create()
        profile = UserProfile.objects.create(
                                             user=user_object,
                                             workplace=new_restaurant
                                             )
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ServerHomeView(TemplateView):
    template_name = 'server_home.html'

    def get_context_data(self):
        context = super(ServerHomeView, self).get_context_data()
        current_server = UserProfile.objects.get(user=self.request.user)
        if current_server.position != 'K':
            current_restaurant = current_server.workplace
            bound_table_list = Table.objects.filter(server__workplace=current_restaurant, fulfilled=False)
            all_tables_list = [x for x in range(1, current_restaurant.number_of_tables + 1)]
            bound_table_numbers = bound_table_list.values_list('number', flat=True)
            unbound_tables = [x for x in all_tables_list if x not in bound_table_numbers]

            context['restaurant'] = current_restaurant
            context['server'] = current_server
            context['menus'] = Menu.objects.all()
            context['bound_tables'] = bound_table_list
            context['unbound_tables'] = unbound_tables
        else:
            return reverse('kitchen')
        return context


# New try at class-based order create view. gonna work this time!!
class CreateOrderItem(CreateView):
    template_name = 'server/order_form.html'
    form_class = CreateOrderForm

    def get_context_data(self, **kwargs):
        context = super(CreateOrderItem, self).get_context_data(**kwargs)
        if self.request.POST:
            
            context['formset'] = OrderFormSet(self.request.POST)
        else:
            context['formset'] = OrderFormSet(initial=[{'quantity': 1}])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return reverse('server_home')
        else:
            return self.render_to_response(self.get_context_data(form=form))


def FunctionBasedCreateOrder(request, table_number):
    server = request.user.userprofile
    OrderFormSet = inlineformset_factory(Table, Order, extra=1, max_num=20, exclude=['delete'])
    menus = Menu.objects.filter(restaurant=request.user.userprofile.workplace)

    if request.method == 'POST':
        new_table = Table.objects.create(server=server, number=table_number)
        order_form_set = OrderFormSet(request.POST, instance=new_table)
        if order_form_set.is_valid():
            order_form_set.save()
        # need to add message if form invalid
        return HttpResponseRedirect(reverse('server_home'))
    else:
        order_form_set = OrderFormSet

        return render(request, 'server/order_form.html', {
                                                          'formset': order_form_set,
                                                          'table_num': table_number,
                                                          'menus': menus,
                                                          }
                      )


def FunctionBasedUpdateOrder(request, table_pk):
    OrderFormSet = inlineformset_factory(Table, form=CreateOrderForm)
    working_table = Table.objects.get(pk=table_pk)

    if request.method == 'POST':
        update_order_form_set = OrderFormSet(request.POST, instance=working_table)
        if update_order_form_set.is_valid():
            update_order_form_set.save()
        return HttpResponseRedirect(reverse('server_home'))
    else:
        update_order_form_set = OrderFormSet(instance=working_table)
        return render(request, 'server/update_order_form.html', {'formset': update_order_form_set})


class OrderDetailView(DetailView):
    model = Order


class KitchenListView(ListView):
    model = Table


class MenuDetailView(DetailView):
    model = Menu


class AddMenuItemView(CreateView):
    model = MenuItem
    fields = ['name', 'description', 'price', 'photo']

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.restaurant = self.request.user.userprofile.workplace
        new_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('server_home')


class CreateMenuView(CreateView):
    model = Menu
    fields = ['name', 'item']

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.restaurant = self.request.user.userprofile.workplace
        new_item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('server_home')


class ServerAddView(CreateView):
    form_class = ServerCreateForm
    model = User
    template_name = 'server/server_create_form.html'

    def form_valid(self, form, **kwargs):
        new_server = form.save()
        server_restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        profile = UserProfile.objects.create(
                                             user=new_server,
                                             name=form.cleaned_data["name"],
                                             workplace=server_restaurant,
                                             position='S'
                                             )
        profile.save()
        return super().form_valid(form, **kwargs)

    def form_invalid(self, form):
        print("Your Form Is Invalid sir!")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('index')


class KitchenAddView(CreateView):
    form_class = ServerCreateForm
    model = User
    template_name = 'server/kitchen_create_form.html'

    def form_valid(self, form, **kwargs):
        new_server = form.save()
        server_restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        profile = UserProfile.objects.create(
                                             user=new_server,
                                             name=form.cleaned_data["name"],
                                             workplace=server_restaurant,
                                             position='K'
                                             )
        profile.save()
        return super().form_valid(form, **kwargs)

    def get_success_url(self):
        return reverse('index')


class UpdateMenuView(UpdateView):
    model = Menu
    fields = ['name', 'item']

    def get_success_url(self, **kwargs):
        return reverse_lazy('menu_detail', kwargs={'pk': self.kwargs['pk']})


class MenuItemDetailView(DetailView):
    model = MenuItem


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['seat_number', 'table_number', 'items']


# class TableStartView(TemplateView):
#     template_name = 'server/table_start_view.html'


def mark_table_fulfilled(request, table_id):
    done_table = Table.objects.get(pk=table_id)
    done_table.fulfilled = True
    done_table.save()
    return HttpResponseRedirect(reverse('kitchen'))


class RestaurantUpdateView(UpdateView):
    model = Restaurant
    fields = '__all__'

    def get_object(self):
        return Restaurant.objects.get(userprofile__workplace=self.request.user.userprofile.workplace)

    def get_success_url(self):
        return reverse('index')
