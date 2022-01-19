library(shiny)
library(rnaturalearth)
library(tidyverse)
# Define UI for application that draws a histogram
ui <- fluidPage(
    
    # Application title
    titlePanel("Swiss Tax Calculator"),
    
    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            selectInput("Income", label = h3("Income"), 
                        choices = c('20000','40000', '60000', '80000', '100000', '200000', '500000'), 
                        selected = '20000'),
            selectInput("Category", label = h3("Category"), 
                        choices = c('Single payer','Family'), 
                        selected = 'Single payer')
        ),
        
        
        # Show a plot of the generated distribution
        mainPanel(
            plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
    
    output$distPlot <- renderPlot({
        swiss_map <- ne_states(country = "Switzerland", returnclass = "sf")
        if (input$Category == 'Single payer') {
            link = '/Users/desmondmolloy/Downloads/Codecademy_classwork/data/single_payer.csv'
        }
        else {
            link = '/Users/desmondmolloy/Downloads/Codecademy_classwork/data/double_payer.csv'
        }
        single_df <- read.csv(link)
        df <- single_df%>%
            filter(Income == as.numeric(input$Income))%>%
            arrange(Canton)
        swiss_map<-swiss_map%>%
            arrange(name)
        df<-df%>%
            mutate(Tax.Status = case_when(
                Swiss.taxes > US.Taxes  ~ "Only Swiss taxes",
                Swiss.taxes <= US.Taxes ~ "Must pay US taxes",
                Swiss.taxes - 6000 > US.Taxes ~ 'Only Swiss taxes with Roth IRA'
            ))
        swiss_map$Tax.Status <- df$Tax.Status
        library(ggplot2)
        
        ggplot(data = swiss_map, aes(fill = `Tax.Status`)) + 
            geom_sf()
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
